import base64
import os
from xml.dom import minidom
import zipfile
import sys

from epub_meta.exceptions import EPubException


IS_PY2 = sys.version_info < (3, 0)


class odict(dict):
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __getattr__(self, attr):
        return self.get(attr)


def iterate_all_tags(root):
    for node in root.childNodes:
        if node.nodeType != node.ELEMENT_NODE:
            continue

        yield node

        for subnode in iterate_all_tags(node):
            yield subnode


def find_tag(xmldoc, tag_name, attr, value):
    # print('Finding tag: <{} {}="{}">'.format(tag_name, attr, value))
    for tag in xmldoc.getElementsByTagName(tag_name):
        if attr in tag.attributes.keys() and tag.attributes[attr].value == value:
            return tag


def find_img_tag(xmldoc, tag_name, attr, value):
    # print('Finding img tag: <{} {}="{}">'.format(tag_name, attr, value))
    for tag in xmldoc.getElementsByTagName(tag_name):
        if attr in tag.attributes.keys() and tag.attributes[attr].value == value:
            if 'href' in tag.attributes.keys():
                filepath = tag.attributes['href'].value
                filename, file_extension = os.path.splitext(filepath)
                if file_extension in ('.gif', '.jpg', '.jpeg', '.png', '.svg'):
                    return filepath, file_extension
    return None, None


def _discover_epub_version(opf_xmldoc):
    try:
        return opf_xmldoc.getElementsByTagName('package')[0].attributes['version'].value
    except (KeyError, IndexError):
        return None


def __discover_dc(opf_xmldoc, name, first_only=True):
    value = None
    try:
        if first_only:
            node = opf_xmldoc.getElementsByTagName(name)[0].firstChild
            if node:
                value = node.nodeValue
        else:
            value = [n.firstChild.nodeValue for n in opf_xmldoc.getElementsByTagName(name) if n.firstChild]
    except (KeyError, IndexError):
        pass
    if not value:
        tag_name = 'dc:{}'.format(name)
        try:
            if first_only:
                node = opf_xmldoc.getElementsByTagName(tag_name)[0].firstChild
                if node:
                    value = node.nodeValue
            else:
                value = [n.firstChild.nodeValue for n in opf_xmldoc.getElementsByTagName(tag_name) if n.firstChild]
        except (KeyError, IndexError):
            pass
    if first_only:
        return value.strip() if value else value
    else:
        return [v.strip() for v in value]


def _discover_title(opf_xmldoc):
    return __discover_dc(opf_xmldoc, 'title')


def _discover_language(opf_xmldoc):
    return __discover_dc(opf_xmldoc, 'language')


def _find_author_from_dom(xmldoc):
    # Only find a single author now with this algorithm but returning a list
    # because that's what caller expects
    authors = []

    # First non-empty child node is author after the author 'tag'
    found_author_tag = False

    for tag in iterate_all_tags(xmldoc):
        if not found_author_tag:
            if tag.nodeName == 'strong' and tag.childNodes and (
               tag.firstChild.nodeType == tag.firstChild.TEXT_NODE) and (
               tag.firstChild.data in ('Author', 'Authors')):

                found_author_tag = True
        else:
            # Find all paragraph tags BEFORE we find another span tag. Those
            # are the author(s).
            if tag.nodeName == 'span':
                break

            if tag.nodeName == 'p' and tag.childNodes and (
               tag.firstChild.nodeType == tag.firstChild.TEXT_NODE):

                data = tag.firstChild.data.strip()
                if data:
                    authors.append(data)

    return authors


def _discover_authors(opf_xmldoc, authors_html=None):
    authors = __discover_dc(opf_xmldoc, 'creator', first_only=False)

    # We've found large portion of books from specific publishers that store
    # the authors in pr02.html in a very specific place.
    if not authors and authors_html is not None:
        authors = _find_author_from_dom(authors_html)

    # Slow and inefficient way to remove duplicates but maintain ordering just
    # in case the author order in epub is significant.
    unique_authors = []
    for author in authors:
        if author not in unique_authors:
            unique_authors.append(author)

    return unique_authors


def _discover_publisher(opf_xmldoc):
    return __discover_dc(opf_xmldoc, 'publisher')


def _find_publish_date_from_dom(xmldoc):
    first_pub = 'First published:'

    for tag in iterate_all_tags(xmldoc):
        if tag.nodeName == 'p' and tag.childNodes and (
           tag.firstChild.nodeType == tag.TEXT_NODE) and (
           tag.firstChild.data.startswith(first_pub)):
            return tag.firstChild.data.split(first_pub)[1].strip()


def _discover_publication_date(opf_xmldoc, date_html=None):
    date = __discover_dc(opf_xmldoc, 'date')

    if not date and date_html is not None:
        date = _find_publish_date_from_dom(date_html)

    return date


def _discover_identifiers(opf_xmldoc):
    # ISBN 10, ISBN 13 etc
    return __discover_dc(opf_xmldoc, 'identifier', first_only=False)


def _discover_subject(opf_xmldoc):
    return __discover_dc(opf_xmldoc, 'subject')


def _discover_cover_image(zf, opf_xmldoc, opf_filepath):
    '''
    Find the cover image path in the OPF file.
    Returns a tuple: (image content in base64, file extension)
    '''
    content = None
    filepath = None
    extension = None

    # Strategies to discover the cover-image path:

    # e.g.: <meta name="cover" content="cover"/>
    tag = find_tag(opf_xmldoc, 'meta', 'name', 'cover')
    if tag and 'content' in tag.attributes.keys():
        item_id = tag.attributes['content'].value
        if item_id:
            # e.g.: <item href="cover.jpg" id="cover" media-type="image/jpeg"/>
            filepath, extension = find_img_tag(opf_xmldoc, 'item', 'id', item_id)
    if not filepath:
        filepath, extension = find_img_tag(opf_xmldoc, 'item', 'id', 'cover-image')
    if not filepath:
        filepath, extension = find_img_tag(opf_xmldoc, 'item', 'id', 'cover')

    # If we have found the cover image path:
    if filepath:
        # The cover image path is relative to the OPF file
        base_dir = os.path.dirname(opf_filepath)
        # print('- Reading Cover Image file: {}/{}'.format(base_dir, filepath))
        content = zf.read(os.path.join(base_dir, filepath))
        content = base64.b64encode(content)

    return content, extension


def _discover_toc(zf, opf_xmldoc, opf_filepath):
    '''
    Returns a list of objects: {title: str, src: str, level: int, index: int}
    '''
    toc = None

    # ePub 3.x
    tag = find_tag(opf_xmldoc, 'item', 'properties', 'nav')
    if tag and 'href' in tag.attributes.keys():
        filepath = tag.attributes['href'].value
        # The xhtml file path is relative to the OPF file
        base_dir = os.path.dirname(opf_filepath)
        # print('- Reading Nav file: {}/{}'.format(base_dir, filepath))
        nav_content = zf.read(os.path.join(base_dir, filepath))
        toc_xmldoc = minidom.parseString(nav_content)

        _toc = []

        for n in toc_xmldoc.getElementsByTagName('a'):
            if n.firstChild and ('href' in n.attributes.keys()):
                href = n.attributes['href'].value
                # Discarding CFI links
                if '.html' in href or '.xhtml' in href:
                    title = n.firstChild.nodeValue
                    # try the second node too (maybe the first child is an empty span)
                    if not title and n.firstChild.firstChild:
                        title = n.firstChild.firstChild.nodeValue

                    title = title.strip() if title else None

                    if title:
                        level = -1
                        parentNode = n.parentNode
                        avoid_infinite_loop = 0 # simple security issue to avoid infinite loop for bad epub files
                        while parentNode and parentNode.nodeName != 'nav' and avoid_infinite_loop < 50:
                            if parentNode.nodeName == 'ol': # count the depth of the a link related to ol items
                                level += 1
                            parentNode = parentNode.parentNode
                            avoid_infinite_loop += 1
                        level = max(level, 0) # root level is 0, not -1

                        _toc.append({'title': title, 'src': href, 'level': level})
        if _toc:
            toc = _toc

    if not toc:
        # ePub 2.x
        tag = find_tag(opf_xmldoc, 'item', 'id', 'ncx')
        if not tag:
            tag = find_tag(opf_xmldoc, 'item', 'id', 'ncxtoc')
        if tag and 'href' in tag.attributes.keys():
            filepath = tag.attributes['href'].value
            # The ncx file path is relative to the OPF file
            base_dir = os.path.dirname(opf_filepath)
            # print('- Reading NCX file: {}/{}'.format(base_dir, filepath))
            ncx_content = zf.read(os.path.join(base_dir, filepath))

            toc_xmldoc = minidom.parseString(ncx_content)

            def read_nav_point(nav_point_node, level = 0):
                items = []
                item = {'title': None, 'src': None, 'level': level}
                children_points = []
                for item_node in nav_point_node.childNodes:
                    if item_node.nodeName in ('navLabel', 'ncx:navLabel'):
                        try:
                            text = item_node.getElementsByTagName('text')[0].firstChild
                        except IndexError:
                            try:
                                text = item_node.getElementsByTagName('ncx:text')[0].firstChild
                            except IndexError:
                                text = None

                        item['title'] = text.nodeValue.strip() if text and text.nodeValue else None
                    elif item_node.nodeName in ('content', 'ncx:content'):
                        if item_node.hasAttribute('src'):
                            item['src'] = item_node.attributes['src'].value
                    elif item_node.nodeName in ('navPoint', 'ncx:navPoint'):
                        children_points.append(item_node)

                if item['title']:
                    items.append(item)
                    for child_node in children_points:
                        subitems = read_nav_point(child_node, level=level + 1)
                        items.extend(subitems)
                return items

            def read_nav_map(toc_xmldoc, level=0):
                items = []
                try:
                    nav_map_node = toc_xmldoc.getElementsByTagName('navMap')[0]
                except IndexError:
                    # Some ebooks use the ncx: namespace so try that too
                    try:
                        nav_map_node = toc_xmldoc.getElementsByTagName('ncx:navMap')[0]
                    except IndexError:
                        print('Failed reading TOC')
                        return items

                for nav_point in nav_map_node.childNodes:
                    if nav_point.nodeName in ('navPoint', 'ncx:navPoint'):
                        subitems = read_nav_point(nav_point, level=level)
                        items.extend(subitems)
                return items

            toc = read_nav_map(toc_xmldoc)

    # add indexes
    if toc:
        for i, t in enumerate(toc):
            t['index'] = i

    return toc


def get_epub_metadata(filepath, read_cover_image=True, read_toc=True):
    '''
    References: http://idpf.org/epub/201 and http://idpf.org/epub/301
    1. Parse META-INF/container.xml file and find the .OPF file path.
    2. In the .OPF file, find the metadata
    '''
    if not zipfile.is_zipfile(filepath):
        raise EPubException('Unknown file')

    # print('Reading ePub file: {}'.format(filepath))
    zf = zipfile.ZipFile(filepath, 'r', compression=zipfile.ZIP_DEFLATED, allowZip64=True)
    container = zf.read('META-INF/container.xml')
    container_xmldoc = minidom.parseString(container)
    # e.g.: <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>
    opf_filepath = container_xmldoc.getElementsByTagName('rootfile')[0].attributes['full-path'].value

    # print('- Reading OPF file: {}'.format(opf_filepath))
    opf = zf.read(opf_filepath)
    opf_xmldoc = minidom.parseString(opf)

    # This file is specific to the authors if it exists.
    authors_html = None
    try:
        authors_html = minidom.parseString(zf.read('OEBPS/pr02.html'))
    except KeyError:
        # Most books store authors using epub tags, so no worries.
        pass

    # This file is specific to the publish date if it exists.
    publish_date_html = None
    try:
        publish_date_html = minidom.parseString(zf.read('OEBPS/pr01.html'))
    except KeyError:
        # Most books store authors using epub tags, so no worries.
        pass


    file_size_in_bytes = os.path.getsize(filepath)

    data = odict({
        'epub_version': _discover_epub_version(opf_xmldoc),
        'title': _discover_title(opf_xmldoc),
        'language': _discover_language(opf_xmldoc),
        'authors': _discover_authors(opf_xmldoc, authors_html=authors_html),
        'publisher': _discover_publisher(opf_xmldoc),
        'publication_date': _discover_publication_date(opf_xmldoc,
                                                       date_html=publish_date_html),
        'identifiers': _discover_identifiers(opf_xmldoc),
        'subject': _discover_subject(opf_xmldoc),
        'file_size_in_bytes': file_size_in_bytes,
    })

    if read_cover_image:
        cover_image_content, cover_image_extension = _discover_cover_image(zf, opf_xmldoc, opf_filepath)
        data.cover_image_content = cover_image_content
        data.cover_image_extension = cover_image_extension

    if read_toc:
        data.toc = _discover_toc(zf, opf_xmldoc, opf_filepath)

    return data


def get_epub_opf_xml(filepath):
    '''
    Returns the file.OPF contents of the ePub file
    '''
    if not zipfile.is_zipfile(filepath):
        raise EPubException('Unknown file')

    # print('Reading ePub file: {}'.format(filepath))
    zf = zipfile.ZipFile(filepath, 'r', compression=zipfile.ZIP_DEFLATED, allowZip64=True)
    container = zf.read('META-INF/container.xml')
    container_xmldoc = minidom.parseString(container)
    # e.g.: <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>
    opf_filepath = container_xmldoc.getElementsByTagName('rootfile')[0].attributes['full-path'].value
    return zf.read(opf_filepath)
