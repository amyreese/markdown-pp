# Author: Cyril Six (sixcy), 2021
# MIT License

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import re
import subprocess

from MarkdownPP.Module import Module
from MarkdownPP.Transform import Transform


def trim_last_newline(s: str) -> str:
    if s[-1] == '\n':
        return s[:-1]
    else:
        return s


class Exec(Module):
    """
    Module for replacing !(EXEC "command") by the result of command
    For example: !(EXEC date)
    """

    execre = re.compile(r'(^|[^\\])!\(EXEC ([^\)]*)\)')

    def transform(self, data):
        transforms = []
        for (n, line) in enumerate(data):
            matches = self.execre.finditer(line)
            content = line
            for match in matches:
                content = self.do_exec(match, content)
            transform = Transform(linenum=n, oper="swap", data=content)
            transforms.append(transform)
        return transforms

    def do_exec(self, match, line):
        execcmd = match.group(2)
        charbefore = match.group(1)
        subp = subprocess.run(execcmd.split(' '), stdout=subprocess.PIPE)
        result = str(subp.stdout, "utf-8")
        result = charbefore + trim_last_newline(result)

        replaced = self.execre.sub(result, line, count=1)
        return replaced
