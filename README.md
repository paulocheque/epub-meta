# epub-meta


[![Build Status](https://travis-ci.org/paulocheque/epub-meta.png?branch=master)](https://travis-ci.org/paulocheque/epub-meta)
[![Coverage Status](https://coveralls.io/repos/paulocheque/epub-meta/badge.png?branch=master)](https://coveralls.io/r/paulocheque/epub-meta?branch=master)
[![Code Status](https://landscape.io/github/paulocheque/epub-meta/master/landscape.png)](https://landscape.io/github/paulocheque/epub-meta/)

**Latest version: 0.0.1 (2016/08)**

Small *Python* library to read *metadata* information from an *ePub* file. 

It does not depends on any library and run on Python 3 and 2.

## Installation

    pip install epub_meta==0.0.1

## Usage

    from epub_meta import get_epub_metadata, get_epub_opf_xml, EPubException

Discover the main metadata of the ePub file

    print(get_epub_metadata('/path/to/my_epub_file.epub'))

Example:

    >>> data = get_epub_metadata('/path/to/pro_git.epub', read_cover_image=True, read_toc=True)
    >>> print(data)

    {
        'authors': [u'Scott Chacon'],
        'epub_version': u'2.0',
        'identifiers': [u'bf50c6e1-eb0a-4a1c-a2cd-ea8809ae086a', u'9781430218333'],
        'language': u'en',
        'publication_date': u'2009-08-19T00:00:00+00:00',
        'publisher': u'Springer',
        'subject': u'Software Development',
        'title': u'Pro Git',
        'cover_image_content': [base64 string],
        'cover_image_extension': '.jpg',
        'toc': [
            u'Pro Git',
            u'Getting Started',
            u'Git Basics',
            u'Git Branching',
            u'Git on the Server',
            u'Distributed Git',
            u'Git Tools',
            u'Customizing Git',
            u'Git and Other Systems',
            u'Git Internals'
        ]
    }

    # You can access the keys like this:
    data.authors
    data.epub_version


To discover and parse yourself the ePub OPF file, you can get the content of the OPF - XML file:

    print(get_epub_opf_xml('/path/to/my_epub_file.epub'))

