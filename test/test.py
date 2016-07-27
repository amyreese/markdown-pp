"""
test.py
-------

Unit testing for MarkdownPP.

"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import unittest
# import os
import re
import subprocess
from MarkdownPP import MarkdownPP
# from tempfile import NamedTemporaryFile

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def read_both_files(filename1, filename2):
    with open(filename1, 'r') as file1, open(filename2, 'r') as file2:
        text1 = file1.read()
        text2 = file2.read()

    return text1, text2


def make_infile_name(m):
    return '{0}/test_{0}.mdpp'.format(m)


def make_outfile_name(m):
    return '{0}/test_{0}.md'.format(m)


def make_targetfile_name(m):
    return '{0}/test_{0}_target.md'.format(m)


def test_prototype(module_name):
    """All modules are tested in the same way."""
    infile_name = make_infile_name(module_name)
    outfile_name = make_outfile_name(module_name)

    with open(infile_name, 'r') as infile, open(outfile_name, 'w+') as outfile:
        MarkdownPP(input=infile, modules=[module_name], output=outfile)

    targetfile_name = make_targetfile_name(module_name)

    return read_both_files(outfile_name, targetfile_name)


class MarkdownPPTests(unittest.TestCase):

    def test_include(self):
        self.assertEqual(*test_prototype('include'))

    def test_includeurl(self):
        self.assertEqual(*test_prototype('includeurl'))

    def test_youtubeembed(self):
        self.assertEqual(*test_prototype('youtubeembed'))

    def test_tableofcontents(self):
        self.assertEqual(*test_prototype('tableofcontents'))

    def test_reference(self):
        self.assertEqual(*test_prototype('reference'))

    def test_latexrender(self):
        input = StringIO('$\displaystyle 1 + 1 = 2 $')
        result_re = (r'!\[\\displaystyle 1 \+ 1 = 2 \]'
                     r'\(http:\/\/quicklatex\.com\/.*\.png "'
                     r'\\displaystyle 1 \+ 1 = 2 "\)')

        output = StringIO()
        MarkdownPP(input=input, modules=['latexrender'], output=output)

        output.seek(0)
        output_str = output.read().strip()
        match = re.match(result_re, output_str)
        self.assertIsNotNone(match)
        self.assertEqual(match.span(), (0, len(output_str)))

    def test_include_shift(self):
        self.assertEqual(*test_prototype('shift'))

        # test shift=2, by shifting again the previous output
        in_string = '!INCLUDE "{}", 1\n'.format(make_outfile_name('shift'))
        input1 = StringIO(in_string)
        output1 = StringIO()
        MarkdownPP(input=input1, modules=['include'], output=output1)

        input2 = StringIO('!INCLUDE "shift/include_me.md", 2\n')
        output2 = StringIO()
        MarkdownPP(input=input2, modules=['include'], output=output2)

        output1.seek(0)
        output2.seek(0)
        self.assertEqual(output1.read(), output2.read())

    def test_script(self):
        # test the script without arguments
        subprocess.call(['markdown-pp', 'script/test_script.mdpp', '-o',
                         'script/test_script.md'])

        self.assertEqual(*read_both_files(make_outfile_name('script'),
                                          make_targetfile_name('script')))

    def test_recursive(self):
        subprocess.call(['markdown-pp', '.', '-r'])

        module_list = ['include', 'includeurl', 'youtubeembed',
                       'tableofcontents', 'reference', 'script', 'shift']
        for module in module_list:
            out, target = read_both_files(make_outfile_name(module),
                                          make_targetfile_name(module))
            self.assertEqual(out, target)


if __name__ == '__main__':
    unittest.main()
