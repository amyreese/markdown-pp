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



if __name__ == '__main__':
    unittest.main()
