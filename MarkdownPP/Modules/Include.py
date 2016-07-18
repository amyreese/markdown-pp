# Copyright 2015 John Reese
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

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

    includere = re.compile("^!INCLUDE\s+(?:\"([^\"]+)\"|'([^']+)')\s*$")

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

    def include(self, match, pwd=""):
        if match.group(1) is None:
            filename = match.group(2)
        else:
            filename = match.group(1)

        if not path.isabs(filename):
            filename = path.join(pwd, filename)

        try:
            f = open(filename, "r")
            data = f.readlines()
            f.close()

            # recursively include file data
            linenum = 0
            for line in data:
                match = self.includere.search(line)
                if match:
                    dirname = path.dirname(filename)
                    data[linenum:linenum+1] = self.include(match, dirname)

                linenum += 1

            return data

        except (IOError, OSError) as exc:
            print(exc)

        return []
