# epub-meta


[![Build Status](https://travis-ci.org/paulocheque/epub-meta.png?branch=master)](https://travis-ci.org/paulocheque/epub-meta)
[![Coverage Status](https://coveralls.io/repos/github/paulocheque/epub-meta/badge.svg?ts=1)](https://coveralls.io/github/paulocheque/epub-meta)
[![Code Status](https://landscape.io/github/paulocheque/epub-meta/master/landscape.png)](https://landscape.io/github/paulocheque/epub-meta/)


**Latest version: 0.0.4 (2016/08)**

Small **Python** library to read **metadata** information from an **ePub** (2 and 3) file. 

It does not depends on any library and run on Python 3 and 2.

## Installation

    pip install epub_meta==0.0.4

## Usage

    from epub_meta import get_epub_metadata, get_epub_opf_xml, EPubException

Discover the main metadata of the ePub file

    >>> metadata = get_epub_metadata('/path/to/my_epub_file.epub')
    >>> type(metadata)
    <dict>
    >>> metadata
    { ... }

Example:

    >>> data = get_epub_metadata('/path/to/pro_git.epub', read_cover_image=True, read_toc=True)
    >>> print(data)

    {
        'authors': [u'Scott Chacon'],
        'epub_version': u'2.0',
        # ISBN, uuids etc
        'identifiers': [u'bf50c6e1-eb0a-4a1c-a2cd-ea8809ae086a', u'9781430218333'],
        'language': u'en',
        'publication_date': u'2009-08-19T00:00:00+00:00',
        'publisher': u'Springer',
        'subject': u'Software Development',
        'title': u'Pro Git',
        # import base64 ; base64.b64decode(data.cover_image_content)
        'cover_image_content': [base64 string],
        'cover_image_extension': '.jpg',
        'toc': [
            {'index': 0, 'title': 'Getting Started', 'src': 'progit_split_000.html', 'level': 0},
            {'index': 1, 'title': 'Git Basics', 'level': 0, 'src': 'progit_split_008.html'},
            {'index': 2, 'title': 'Git Branching', 'level': 0, 'src': 'progit_split_017.html'},
            {'index': 3, 'title': 'Git on the Server', 'src': 'progit_split_025.html', 'level': 0},
            {'index': 4, 'title': 'Distributed Git', 'src': 'progit_split_037.html', 'level': 0},
            {'index': 5, 'title': 'Git Tools', 'src': 'progit_split_042.html', 'index': 5, 'level': 0},
            {'index': 6, 'title': 'Customizing Git', 'src': 'progit_split_051.html', 'level': 0},
            {'index': 7, 'title': 'Git and Other Systems', 'src': 'progit_split_057.html', 'level': 0},
            {'index': 8, 'title': 'Git Internals', 'src': 'progit_split_061.html', 'level': 0}
        ],
        'file_size_in_bytes': 4346158
    }

You can access the dict keys using *dot* notation:

    data.authors
    data.epub_version
    ...

You should check for invalid ePub files or for unknown ePub conventions:

    try:
        get_epub_metadata('/path/to/my_epub_file.epub')    
    except EPubException as e:
        print(e)

To discover and parse yourself the ePub OPF file, you can get the content of the *OPF - XML* file:

    print(get_epub_opf_xml('/path/to/my_epub_file.epub'))


## Change Log

##### 0.0.4 (2016-11-02)

- Backward incompatibility: Returning ToC as a list of objects instead of a list of strings
- The ToC information includes the source of the section: property `src`
- The ToC is hierarchical, so we include a `level` property to identify the depth of the toc item in the list
- The ToC order is important, so we include a `index` property to keep the order explicit
- Trimming some string values

##### 0.0.3 (2016-08-23)

- Added the file size into the metadata dict

##### 0.0.2 (2016-08-22)

- Fixed TOC discovering for ePub v3 files

##### 0.0.1 (2016-08-19)

- `get_epub_metadata(path, read_cover_image=True, read_toc=True)` function
- `get_epub_opf_xml(path)` function
- Read cover image content in base64
- Read TOC contents as an list of strings


## Development

Useful commands:

    # Create a virtual env
    make prepare

    # Install al dependencies
    make deps

    # Run tests
    make test

    # Run tests with Tox (for all Python compatible versions)
    make test_all

    # Run coverage
    make coverage

    # Useful command for running tests before pushing to Git
    make push
