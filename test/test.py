"""
test.py
-------

Unit testing for MarkdownPP.

"""

import unittest
import os
from MarkdownPP import MarkdownPP
from io import StringIO


class MarkdownPPTests(unittest.TestCase):

    def test_include(self):
        output = StringIO()

        MarkdownPP(input=StringIO('foobar\n!INCLUDE "test_include.md"\n'),
                   modules=['include'],
                   output=output)

        output.seek(0)
        self.assertEqual(output.read(), 'foobar\nThis is a test.\n')

    def test_include_url(self):
        output = StringIO()
        path = os.path.join(os.getcwd(), "test_include.md")

        MarkdownPP(input=StringIO('foobar\n!INCLUDEURL "file://{}"\n'.format(path)),
                   modules=['includeurl'],
                   output=output)

        output.seek(0)
        self.assertEqual(output.read(), 'foobar\nThis is a test.\n')



if __name__ == '__main__':
    unittest.main()
