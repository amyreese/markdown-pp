"""
test.py
-------

Unit testing for MarkdownPP.

"""

import unittest
import os
import re
from MarkdownPP import MarkdownPP
from io import StringIO


class MarkdownPPTests(unittest.TestCase):

    def test_include(self):
        input = StringIO('foobar\n!INCLUDE "test_include.md"\n')
        result = 'foobar\nThis is a test.\n'

        output = StringIO()
        MarkdownPP(input=input, modules=['include'], output=output)

        output.seek(0)
        self.assertEqual(output.read(), result)

    def test_include_url(self):
        path = os.path.join(os.getcwd(), "test_include.md")
        input = StringIO('foobar\n!INCLUDEURL "file://{}"\n'.format(path))
        result = 'foobar\nThis is a test.\n'

        output = StringIO()
        MarkdownPP(input=input, modules=['includeurl'], output=output)

        output.seek(0)
        self.assertEqual(output.read(), result)

    def test_youtube(self):
        input = StringIO('foobar\n!VIDEO "http://www.youtube.com/embed/7aEYoP5-duY"\n')
        result = 'foobar\n[![Link to Youtube video](images/youtube/7aEYoP5-duY.png)](http://www.youtube.com/watch?v=7aEYoP5-duY)\n'

        output = StringIO()
        MarkdownPP(input=input, modules=['youtubeembed'], output=output)

        output.seek(0)
        self.assertEqual(output.read(), result)

    def test_toc(self):
        input = StringIO('\n# Document Title\n\n'
                         '!TOC\n\n'
                         '## Header 1\n'
                         '### Header 1.a\n'
                         '## Header 2\n')

        result = """
        # Document Title

        1\.  [Header 1](#header1)
        1.1\.  [Header 1.a](#header1.a)
        2\.  [Header 2](#header2)

        <a name="header1"></a>

        ## 1\. Header 1
        <a name="header1.a"></a>

        ### 1.1\. Header 1.a
        <a name="header2"></a>

        ## 2\. Header 2"""

        output = StringIO()
        MarkdownPP(input=input, modules=['tableofcontents'], output=output)

        output.seek(0)
        self.assertEqual([l.strip() for l in output.readlines()],
                         [l.strip() for l in result.split('\n')])

    def test_reference(self):
        input = StringIO('\n!REF\n\n[github]: http://github.com "GitHub"')
        result = '\n*\t[GitHub][github]\n\n[github]: http://github.com "GitHub"'

        output = StringIO()
        MarkdownPP(input=input, modules=['reference'], output=output)

        output.seek(0)
        self.assertEqual(output.read(), result)

    def test_latexrender(self):
        input = StringIO('$\displaystyle 1 + 1 = 2 $')
        result_re = r'!\[\\displaystyle 1 \+ 1 = 2 \]\(http:\/\/quicklatex\.com\/.*\.png "\\displaystyle 1 \+ 1 = 2 "\)'

        output = StringIO()
        MarkdownPP(input=input, modules=['latexrender'], output=output)

        output.seek(0)
        output_str = output.read().strip()
        match = re.match(result_re, output_str)
        self.assertIsNotNone(match)
        self.assertEqual(match.span(), (0, len(output_str)))



if __name__ == '__main__':
    unittest.main()
