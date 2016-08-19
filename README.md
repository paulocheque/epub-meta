# epub-meta


[![Build Status](https://travis-ci.org/paulocheque/epub-meta.png?branch=master)](https://travis-ci.org/paulocheque/epub-meta)
[![Coverage Status](https://coveralls.io/repos/github/paulocheque/epub-meta/badge.svg)](https://coveralls.io/github/paulocheque/epub-meta)
[![Code Status](https://landscape.io/github/paulocheque/epub-meta/master/landscape.png)](https://landscape.io/github/paulocheque/epub-meta/)


**Latest version: 0.0.1 (2016/08)**

Small **Python** library to read **metadata** information from an **ePub** (2 and 3) file. 

It does not depends on any library and run on Python 3 and 2.

## Installation

    pip install epub_meta==0.0.1

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
