
if __name__ == '__main__':
    import sys
    from pprint import pprint
    from epub_meta import get_epub_metadata
    dirpath = sys.argv[1]
    data = get_epub_metadata(dirpath, read_cover_image=False, read_toc=True)
    pprint(data)
