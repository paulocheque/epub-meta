import base64
import os
from xml.dom import minidom
import zipfile

from epub_meta.exceptions import EPubException


class odict(dict):
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __getattr__(self, attr):
        return self.get(attr)


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
    return value


def _discover_title(opf_xmldoc):
    return __discover_dc(opf_xmldoc, 'title')


def _discover_language(opf_xmldoc):
    return __discover_dc(opf_xmldoc, 'language')


def _discover_authors(opf_xmldoc):
    return __discover_dc(opf_xmldoc, 'creator', first_only=False)


def _discover_publisher(opf_xmldoc):
    return __discover_dc(opf_xmldoc, 'publisher')


def _discover_publication_date(opf_xmldoc):
    return __discover_dc(opf_xmldoc, 'date')


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
                    _toc.append(n.firstChild.nodeValue)
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
            toc = [n.firstChild.nodeValue for n in toc_xmldoc.getElementsByTagName('text') if n.firstChild]

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

    data = odict({
        'epub_version': _discover_epub_version(opf_xmldoc),
        'title': _discover_title(opf_xmldoc),
        'language': _discover_language(opf_xmldoc),
        'authors': _discover_authors(opf_xmldoc),
        'publisher': _discover_publisher(opf_xmldoc),
        'publication_date': _discover_publication_date(opf_xmldoc),
        'identifiers': _discover_identifiers(opf_xmldoc),
        'subject': _discover_subject(opf_xmldoc),
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
