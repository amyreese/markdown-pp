"""
test.py
-------

Unit testing for MarkdownPP.

"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import unittest
import os
import re
import subprocess
from MarkdownPP import MarkdownPP
from tempfile import NamedTemporaryFile

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
        # test shift=1
        input = StringIO('!INCLUDE "datafiles/test_shift.mdpp", 1\n')
        with open('datafiles/test_shift.md', 'r') as resfile:
            result = resfile.read()

        output = StringIO()
        MarkdownPP(input=input, modules=['include'], output=output)

        output.seek(0)
        self.assertEqual(output.read(), result)

        # test shift=2, by shifting again the previous output
        output.seek(0)
        with NamedTemporaryFile(delete=False) as temp:
            temp.write(output.read().encode('utf-8'))
            name = temp.name

        input1 = StringIO('!INCLUDE "{}", 1\n'.format(name))
        output1 = StringIO()
        MarkdownPP(input=input1, modules=['include'], output=output1)

        input2 = StringIO('!INCLUDE "datafiles/test_shift.mdpp", 2\n')
        output2 = StringIO()
        MarkdownPP(input=input2, modules=['include'], output=output2)

        output1.seek(0)
        output2.seek(0)

        self.assertEqual(output1.read(), output2.read())
        os.remove(name)

    def test_script(self):
        # test the script without arguments
        with NamedTemporaryFile(delete=False) as temp_outfile:
            subprocess.call(['markdown-pp', 'datafiles/test_script.mdpp', '-o',
                            temp_outfile.name])

            with open('datafiles/test_script_target.md', 'r') as targetfile:
                target = targetfile.read()

            temp_outfile.seek(0)
            self.assertEqual(target, temp_outfile.read().decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
