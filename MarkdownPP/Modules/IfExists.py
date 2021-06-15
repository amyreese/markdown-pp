# Copyright 2015 John Reese
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import glob
import re
from os import path

from MarkdownPP.Module import Module
from MarkdownPP.Transform import Transform


class IfExists(Module):
    """
    Module that tests for a file existence. If the file exists, all the lines
    following the tag are included, until the end tag is found.
     If the file does not exist, the entire block is skipped.
    """

    # matches !INCLUDE directives in .mdpp files
    ifexistsre = re.compile(r"^!IFEXISTS\s+(?:\"([^\"]+)\"|'([^']+)')\s*$")
    endifexistsre = re.compile(r"^!ENDIFEXISTS\s*")

    def transform(self, data):
        transforms = []
        skip_content = False
        in_block = False
        linenum = -1
        for line in data:
            drop_line = False
            linenum += 1
            match = self.ifexistsre.search(line)
            if match:
                drop_line = True
                in_block = True
                if not self.file_exists(match):
                    skip_content = True
            else:
                if in_block:
                    match = self.endifexistsre.search(line)
                    if match:
                        skip_content = False
                        drop_line = True
            if skip_content or drop_line:
                transform = Transform(linenum=linenum, oper="drop")
                transforms.append(transform)

        return transforms

    def file_exists(self, match, pwd=""):
        # file name is caught in group 1 if it's written with double quotes,
        # or group 2 if written with single quotes
        fileglob = match.group(1) or match.group(2)

        result = False
        if pwd != "":
            fileglob = path.join(pwd, fileglob)

        files = sorted(glob.glob(fileglob))
        if len(files) > 0:
            result = True

        return result
