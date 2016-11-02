# coding: utf-8
import os
import json
import unittest

from epub_meta import get_epub_metadata, get_epub_opf_xml, EPubException
from epub_meta.collector import IS_PY2


dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../samples')


class GetEPubMetadataTests(unittest.TestCase):
    def test_inexistent_file(self):
        try:
            get_epub_metadata(os.path.join(dir_path, 'inexistent.epub'))
            self.assertEqual(1, 0)
        except EPubException:
            pass

    def test_epub_version(self):
        data = get_epub_metadata(os.path.join(dir_path, 'backbone-fundamentals.epub'))
        self.assertEqual(data.epub_version, '2.0')
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-cfi-20120521.epub'))
        self.assertEqual(data.epub_version, '3.0')
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-pls-ssml-20120322.epub'))
        self.assertEqual(data.epub_version, '3.0')
        data = get_epub_metadata(os.path.join(dir_path, 'mathjax_tests.epub'))
        self.assertEqual(data.epub_version, '3.0')
        data = get_epub_metadata(os.path.join(dir_path, 'moby-dick.epub'))
        self.assertEqual(data.epub_version, '3.0')
        data = get_epub_metadata(os.path.join(dir_path, 'progit.epub'))
        self.assertEqual(data.epub_version, '2.0')

        data = get_epub_metadata(os.path.join(dir_path, 'high-performance-computing-5.2.epub'))
        self.assertEqual(data.epub_version, '2.0')

    def test_title(self):
        data = get_epub_metadata(os.path.join(dir_path, 'backbone-fundamentals.epub'))
        self.assertEqual(data.title, 'Developing Backbone.js Applications')
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-cfi-20120521.epub'))
        self.assertEqual(data.title, 'Georgia')
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-pls-ssml-20120322.epub'))
        self.assertEqual(data.title, 'Georgia')
        data = get_epub_metadata(os.path.join(dir_path, 'mathjax_tests.epub'))
        self.assertEqual(data.title, 'Gathering a few MathML torture tests -- no MathJax')
        data = get_epub_metadata(os.path.join(dir_path, 'moby-dick.epub'))
        self.assertEqual(data.title, 'Moby-Dick')
        data = get_epub_metadata(os.path.join(dir_path, 'progit.epub'))
        self.assertEqual(data.title, 'Pro Git')
        data = get_epub_metadata(os.path.join(dir_path, 'high-performance-computing-5.2.epub'))
        self.assertEqual(data.title, 'High Performance Computing')

    def test_language(self):
        data = get_epub_metadata(os.path.join(dir_path, 'backbone-fundamentals.epub'))
        self.assertEqual(data.language, 'en-US')
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-cfi-20120521.epub'))
        self.assertEqual(data.language, 'en-US')
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-pls-ssml-20120322.epub'))
        self.assertEqual(data.language, 'en-US')
        data = get_epub_metadata(os.path.join(dir_path, 'mathjax_tests.epub'))
        self.assertEqual(data.language, 'en')
        data = get_epub_metadata(os.path.join(dir_path, 'moby-dick.epub'))
        self.assertEqual(data.language, 'en-US')
        data = get_epub_metadata(os.path.join(dir_path, 'progit.epub'))
        self.assertEqual(data.language, 'en')
        data = get_epub_metadata(os.path.join(dir_path, 'high-performance-computing-5.2.epub'))
        self.assertEqual(data.language, 'en')

    def test_authors(self):
        data = get_epub_metadata(os.path.join(dir_path, 'backbone-fundamentals.epub'))
        self.assertEqual(data.authors, ['Addy Osmani'])
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-cfi-20120521.epub'))
        self.assertEqual(data.authors, ['Various'])
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-pls-ssml-20120322.epub'))
        self.assertEqual(data.authors, ['Various'])
        data = get_epub_metadata(os.path.join(dir_path, 'mathjax_tests.epub'))
        self.assertEqual(data.authors, ['Peter Krautzberger'])
        data = get_epub_metadata(os.path.join(dir_path, 'moby-dick.epub'))
        self.assertEqual(data.authors, ['Herman Melville'])
        data = get_epub_metadata(os.path.join(dir_path, 'progit.epub'))
        self.assertEqual(data.authors, ['Scott Chacon'])
        data = get_epub_metadata(os.path.join(dir_path, 'high-performance-computing-5.2.epub'))
        self.assertEqual(data.authors, ['Charles Severance', 'Kevin Dowd'])

    def test_publisher(self):
        data = get_epub_metadata(os.path.join(dir_path, 'backbone-fundamentals.epub'))
        self.assertEqual(data.publisher, None)
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-cfi-20120521.epub'))
        self.assertEqual(data.publisher, None)
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-pls-ssml-20120322.epub'))
        self.assertEqual(data.publisher, None)
        data = get_epub_metadata(os.path.join(dir_path, 'mathjax_tests.epub'))
        self.assertEqual(data.publisher, None)
        data = get_epub_metadata(os.path.join(dir_path, 'moby-dick.epub'))
        self.assertEqual(data.publisher, 'Harper & Brothers, Publishers')
        data = get_epub_metadata(os.path.join(dir_path, 'progit.epub'))
        self.assertEqual(data.publisher, 'Springer')
        data = get_epub_metadata(os.path.join(dir_path, 'high-performance-computing-5.2.epub'))
        self.assertEqual(data.publisher, None)

    def test_publication_date(self):
        data = get_epub_metadata(os.path.join(dir_path, 'backbone-fundamentals.epub'))
        self.assertEqual(data.publication_date, None)
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-cfi-20120521.epub'))
        self.assertEqual(data.publication_date, None)
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-pls-ssml-20120322.epub'))
        self.assertEqual(data.publication_date, None)
        data = get_epub_metadata(os.path.join(dir_path, 'mathjax_tests.epub'))
        self.assertEqual(data.publication_date, None)
        data = get_epub_metadata(os.path.join(dir_path, 'moby-dick.epub'))
        self.assertEqual(data.publication_date, None)
        data = get_epub_metadata(os.path.join(dir_path, 'progit.epub'))
        self.assertEqual(data.publication_date, '2009-08-19T00:00:00+00:00')
        data = get_epub_metadata(os.path.join(dir_path, 'high-performance-computing-5.2.epub'))
        self.assertEqual(data.publication_date, None)

    def test_identifiers(self):
        data = get_epub_metadata(os.path.join(dir_path, 'backbone-fundamentals.epub'))
        self.assertEqual(data.identifiers, ['urn:uuid:d1d91a1f-031f-49c0-83ff-2f556aa0c4d5'])
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-cfi-20120521.epub'))
        self.assertEqual(data.identifiers, ['code.google.com.epub-samples.georgia-cfi'])
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-pls-ssml-20120322.epub'))
        self.assertEqual(data.identifiers, ['code.google.com.epub-samples.georgia-pls-ssml'])
        data = get_epub_metadata(os.path.join(dir_path, 'mathjax_tests.epub'))
        self.assertEqual(data.identifiers, ['http://boolesrings.org/krautzberger'])
        data = get_epub_metadata(os.path.join(dir_path, 'moby-dick.epub'))
        self.assertEqual(data.identifiers, ['code.google.com.epub-samples.moby-dick-basic'])
        data = get_epub_metadata(os.path.join(dir_path, 'progit.epub'))
        self.assertEqual(data.identifiers, ['bf50c6e1-eb0a-4a1c-a2cd-ea8809ae086a', '9781430218333'])
        data = get_epub_metadata(os.path.join(dir_path, 'high-performance-computing-5.2.epub'))
        self.assertEqual(data.identifiers, ['_id253509'])

    def test_subject(self):
        data = get_epub_metadata(os.path.join(dir_path, 'backbone-fundamentals.epub'))
        self.assertEqual(data.subject, None)
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-cfi-20120521.epub'))
        self.assertEqual(data.subject, None)
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-pls-ssml-20120322.epub'))
        self.assertEqual(data.subject, None)
        data = get_epub_metadata(os.path.join(dir_path, 'mathjax_tests.epub'))
        self.assertEqual(data.subject, None)
        data = get_epub_metadata(os.path.join(dir_path, 'moby-dick.epub'))
        self.assertEqual(data.subject, None)
        data = get_epub_metadata(os.path.join(dir_path, 'progit.epub'))
        self.assertEqual(data.subject, 'Software Development')
        data = get_epub_metadata(os.path.join(dir_path, 'high-performance-computing-5.2.epub'))
        self.assertEqual(data.subject, None)

    def test_cover_image(self):
        data = get_epub_metadata(os.path.join(dir_path, 'backbone-fundamentals.epub'))
        self.assertEqual(data.cover_image_extension, '.jpg')
        self.assertIsNotNone(data.cover_image_content)
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-cfi-20120521.epub'))
        self.assertEqual(data.cover_image_extension, '.png')
        self.assertIsNotNone(data.cover_image_content)
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-pls-ssml-20120322.epub'))
        self.assertEqual(data.cover_image_extension, '.png')
        self.assertIsNotNone(data.cover_image_content)
        data = get_epub_metadata(os.path.join(dir_path, 'mathjax_tests.epub'))
        self.assertEqual(data.cover_image_extension, None)
        self.assertEqual(data.cover_image_content, None)
        data = get_epub_metadata(os.path.join(dir_path, 'moby-dick.epub'))
        self.assertEqual(data.cover_image_extension, '.jpg')
        self.assertIsNotNone(data.cover_image_content)
        data = get_epub_metadata(os.path.join(dir_path, 'progit.epub'))
        self.assertEqual(data.cover_image_extension, '.jpg')
        self.assertIsNotNone(data.cover_image_content)
        data = get_epub_metadata(os.path.join(dir_path, 'high-performance-computing-5.2.epub'))
        self.assertEqual(data.cover_image_extension, '.png')
        self.assertIsNotNone(data.cover_image_content)

    def test_toc(self):
        data = get_epub_metadata(os.path.join(dir_path, 'backbone-fundamentals.epub'))
        self.assertEqual(data.toc, [
            {'index': 0, 'title': 'Title Page', 'src': 'title_page.xhtml', 'level': 0},
            {'title': 'MongoDB Ruby Driver', 'index': 1, 'src': 'ch2.xhtml', 'level': 0},
            {'index': 2, 'level': 0, 'title': 'Practical', 'src': 'ch3.xhtml'},
            {'title': 'Unit Testing Backbone Applications With Jasmine', 'index': 3, 'src': 'ch4.xhtml', 'level': 0},
            {'title': 'Unit Testing Backbone Applications With QUnit And SinonJS', 'src': 'ch5.xhtml', 'level': 0, 'index': 4},
            {'level': 0, 'index': 5, 'src': 'ch6.xhtml', 'title': 'QUnit'},
            {'title': 'SinonJS', 'src': 'ch7.xhtml', 'level': 0, 'index': 6},
            {'level': 0, 'title': 'Practical', 'index': 7, 'src': 'ch8.xhtml'}
        ])
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-cfi-20120521.epub'))
        self.assertEqual(len(data.toc), 10)
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-pls-ssml-20120322.epub'))
        self.assertEqual(len(data.toc), 17)
        data = get_epub_metadata(os.path.join(dir_path, 'mathjax_tests.epub'))
        self.assertEqual(len(data.toc), 6)
        data = get_epub_metadata(os.path.join(dir_path, 'moby-dick.epub'))
        self.assertEqual(len(data.toc), 143)
        data = get_epub_metadata(os.path.join(dir_path, 'progit.epub'))
        self.assertEqual(data.toc, [
            {'src': 'progit_split_000.html', 'title': 'Getting Started', 'level': 0, 'index': 0},
            {'title': 'Git Basics', 'level': 0, 'src': 'progit_split_008.html', 'index': 1},
            {'index': 2, 'title': 'Git Branching', 'level': 0, 'src': 'progit_split_017.html'},
            {'title': 'Git on the Server', 'src': 'progit_split_025.html', 'level': 0, 'index': 3},
            {'title': 'Distributed Git', 'src': 'progit_split_037.html', 'level': 0, 'index': 4},
            {'src': 'progit_split_042.html', 'title': 'Git Tools', 'index': 5, 'level': 0},
            {'src': 'progit_split_051.html', 'title': 'Customizing Git', 'level': 0, 'index': 6},
            {'index': 7, 'src': 'progit_split_057.html', 'title': 'Git and Other Systems', 'level': 0},
            {'index': 8, 'title': 'Git Internals', 'src': 'progit_split_061.html', 'level': 0}
        ])

        data = get_epub_metadata(os.path.join(dir_path, 'high-performance-computing-5.2.epub'))
        self.assertEqual(data.toc, [
            {"src": "index.html", "level": 0, "index": 0, "title": "High Performance Computing"},
            {"src": "pr01.html", "level": 1, "index": 1, "title": "Introduction to the Connexions Edition"},
            {"src": "pr02.html", "level": 1, "index": 2, "title": "Introduction to High Performance Computing"},
            {"src": "ch01.html", "level": 1, "index": 3, "title": "1. Modern Computer Architectures"},
            {"src": "ch02.html", "level": 1, "index": 4, "title": "2. Programming and Tuning Software"},
            {"src": "ch03.html", "level": 1, "index": 5, "title": "3. Shared-Memory Parallel Processors"},
            {"src": "ch04.html", "level": 1, "index": 6, "title": "4. Scalable Parallel Processing"},
            {"src": "ch05.html", "level": 1, "index": 7, "title": "5. Appendixes"},
            {"src": "ix01.html", "level": 1, "index": 8, "title": "Index"},
            {"src": "co01.html", "level": 1, "index": 9, "title": "Attributions"},
            {"src": "co02.html", "level": 1, "index": 10, "title": "About Connexions"}
        ])

    def test_file_size(self):
        data = get_epub_metadata(os.path.join(dir_path, 'backbone-fundamentals.epub'))
        self.assertEqual(data.file_size_in_bytes, 325803)
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-cfi-20120521.epub'))
        self.assertEqual(data.file_size_in_bytes, 1095025)
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-pls-ssml-20120322.epub'))
        self.assertEqual(data.file_size_in_bytes, 546553)
        data = get_epub_metadata(os.path.join(dir_path, 'mathjax_tests.epub'))
        self.assertEqual(data.file_size_in_bytes, 809373)
        data = get_epub_metadata(os.path.join(dir_path, 'moby-dick.epub'))
        self.assertEqual(data.file_size_in_bytes, 1670383)
        data = get_epub_metadata(os.path.join(dir_path, 'progit.epub'))
        self.assertEqual(data.file_size_in_bytes, 4346158)
        data = get_epub_metadata(os.path.join(dir_path, 'high-performance-computing-5.2.epub'))
        self.assertEqual(data.file_size_in_bytes, 3045262)

    def test_encoding(self):
        data = get_epub_metadata(os.path.join(dir_path, 'progit.epub'))
        if IS_PY2:
            self.assertEqual(type(data.title), unicode)
            self.assertEqual(type(data.toc[0]), dict)
            self.assertEqual(type(data.toc[1]), dict)
        else:
            self.assertEqual(type(data.title), str)
            self.assertEqual(type(data.toc[0]), dict)
            self.assertEqual(type(data.toc[1]), dict)


class GetOpfXmlTests(unittest.TestCase):
    def test_inexistent_file(self):
        try:
            get_epub_opf_xml(os.path.join(dir_path, 'inexistent.epub'))
            self.assertEqual(1, 0)
        except EPubException:
            pass

    def test_inexistent_file(self):
        xml = get_epub_opf_xml(os.path.join(dir_path, 'progit.epub'))
        self.assertTrue(xml.startswith(b'<?xml version=\'1.0\' encoding=\'utf-8'))


class PrintEPubMetadataTests(unittest.TestCase):
    def test_run(self):
        samples = ('backbone-fundamentals.epub', 'georgia-cfi-20120521.epub', 'georgia-pls-ssml-20120322.epub',
            'mathjax_tests.epub', 'moby-dick.epub', 'progit.epub')
        for sample in samples:
            data = get_epub_metadata(os.path.join(dir_path, sample), read_cover_image=False, read_toc=True)
            print(json.dumps(data, indent=4))
