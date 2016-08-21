# coding: utf-8
import os
import unittest
from pprint import pprint

from epub_meta import get_epub_metadata, get_epub_opf_xml, EPubException


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

    def test_toc(self):
        data = get_epub_metadata(os.path.join(dir_path, 'backbone-fundamentals.epub'))
        self.assertEqual(data.toc, ['Title Page', 'MongoDB Ruby Driver', 'Practical', 'Unit Testing Backbone Applications With Jasmine', 'Unit Testing Backbone Applications With QUnit And SinonJS', 'QUnit', 'SinonJS', 'Practical'])
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-cfi-20120521.epub'))
        self.assertEqual(len(data.toc), 10)
        data = get_epub_metadata(os.path.join(dir_path, 'georgia-pls-ssml-20120322.epub'))
        self.assertEqual(len(data.toc), 17)
        data = get_epub_metadata(os.path.join(dir_path, 'mathjax_tests.epub'))
        self.assertEqual(len(data.toc), 6)
        data = get_epub_metadata(os.path.join(dir_path, 'moby-dick.epub'))
        self.assertEqual(len(data.toc), 143)
        data = get_epub_metadata(os.path.join(dir_path, 'progit.epub'))
        self.assertEqual(data.toc, ['Pro Git', 'Getting Started', 'Git Basics', 'Git Branching', 'Git on the Server', 'Distributed Git', 'Git Tools', 'Customizing Git', 'Git and Other Systems', 'Git Internals'])


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
            pprint(data)
