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


class Include(Module):
    """
    Module for recursively including the contents of other files into the
    current document using a command like `!INCLUDE "path/to/filename"`.
    Target paths can be absolute or relative to the file containing the command
    """

    # matches !INCLUDE directives in .mdpp files
    includere = re.compile(r"^!INCLUDE\s+(?:\"([^\"]+)\"|'([^']+)')"
                           r"\s*(?:,\s*(\d+))?\s*$")

    # matches title lines in Markdown files
    titlere = re.compile(r"^(:?#+.*|={3,}|-{3,})$")

    # matches unescaped formatting characters such as ` or _
    formatre = re.compile(r"[^\\]?[_*`]")

    # matches code block start and stop
    #  code blocks can also be indented by 4 spaces or a tab
    # in which case we don't car because it does not match titlere
    codeblockre = re.compile(r"```")

    # includes should happen before anything else
    priority = 0

    def transform(self, data):
        transforms = []

        linenum = 0
        for line in data:
            match = self.includere.search(line)
            if match:
                includedata = self.include(match)

                transform = Transform(linenum=linenum, oper="swap",
                                      data=includedata)
                transforms.append(transform)

            linenum += 1

        return transforms

    def include_file(self, filename, pwd="", shift=0):
        try:
            f = open(filename, "r", encoding = self.encoding)
            data = f.readlines()
            f.close()
            in_codeblock = False

            # line by line, apply shift and recursively include file data
            linenum = 0
            includednum = 0
            for line in data:
                match = self.includere.search(line)

                if self.codeblockre.search(line):
                    in_codeblock = not in_codeblock

                if match:
                    dirname = path.dirname(filename)
                    data[linenum:linenum+1] = self.include(match, dirname)
                    includednum = linenum
                    # Update line so that we won't miss a shift if
                    # heading is on the 1st line.
                    line = data[linenum]

                if shift:

                    titlematch = self.titlere.search(line)
                    if titlematch and not in_codeblock:
                        to_del = []
                        for _ in range(shift):
                            # Skip underlines with empty above text
                            # or underlines that are the first line of an
                            # included file
                            prevtxt = re.sub(self.formatre, '',
                                             data[linenum - 1]).strip()
                            isunderlined = prevtxt and linenum > includednum
                            if data[linenum][0] == '#':
                                data[linenum] = "#" + data[linenum]
                            elif data[linenum][0] == '=' and isunderlined:
                                data[linenum] = data[linenum].replace("=", '-')
                            elif data[linenum][0] == '-' and isunderlined:
                                data[linenum] = '### ' + data[linenum - 1]
                                to_del.append(linenum - 1)
                        for l in to_del:
                            del data[l]

                linenum += 1

            return data

        except (IOError, OSError) as exc:
            print(exc)

        return []

    def include(self, match, pwd=""):
        # file name is caught in group 1 if it's written with double quotes,
        # or group 2 if written with single quotes
        fileglob = match.group(1) or match.group(2)

        shift = int(match.group(3) or 0)

        result = []
        if pwd != "":
            fileglob = path.join(pwd, fileglob)

        files = sorted(glob.glob(fileglob))
        if len(files) > 0:
            for filename in files:
                result += self.include_file(filename, pwd, shift)
        else:
            result.append("")

        return result
