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
    if len(s) > 0 and s[-1] == '\n':
        return s[:-1]
    else:
        return s


class Exec(Module):
    """
    Module for replacing !(EXEC "command") by the result of command
    For example: !(EXEC date)
    """

    # Matches either !(EXEC cmd) or ![EXEC cmd] or !{EXEC cmd}
    # Doesn't match if it's a \! instead of a !
    # Also, if it's say ![EXEC cmd], then cmd should not have any ']' or else
    #   the result will be wrong
    # (I don't think there is a way to have a user-friendly mistake checker
    # without coding a whole grammar)
    #
    # Groups:
    #   (1) The potential character before '!'
    #   (2) The whole (EXEC cmd) match (or [EXEC cmd], etc..)
    #   (3) If it's a parenthesis match, the cmd
    #   (4) If it's a bracket match, the cmd
    #   (5) If it's a brace match, the cmd
    withpar = r'\(EXEC ([^\)]*)\)'
    withbrackets = r'\[EXEC ([^\]]*)\]'
    withbraces = r'\{EXEC ([^\}]*)\}'
    execre = re.compile(r'(^|[^\\])!'
                        + r'({}|{}|{})'
                        .format(withpar, withbrackets, withbraces))

    # Same as above, but matches specifically those that were escaped
    # For example: \!(EXEC cmd)
    #
    # Groups:
    #   (1) The whole (EXEC cmd)
    #   (2+) Shouldn't matter, but same as above
    escapedexecre = re.compile(r'\\!'
                               + r'({}|{}|{})'
                               .format(withpar, withbrackets, withbraces))

    def transform(self, data):
        transforms = []
        for (n, line) in enumerate(data):
            # Substitution of all !EXEC(...)
            matches = self.execre.finditer(line)
            content = line
            for match in matches:
                content = self.do_exec(match, content)

            # Renaming \!EXEC(..) -> !EXEC(..)
            matches = self.escapedexecre.finditer(line)
            for match in matches:
                content = self.rename_escaped(match, content)

            transform = Transform(linenum=n, oper="swap", data=content)
            transforms.append(transform)
        return transforms

    def rename_escaped(self, match, line):
        return self.escapedexecre.sub("!" + match.group(1), line, count=1)

    def do_exec(self, match, line):
        # Find the right group
        for i in range(3, 6):
            execcmd = match.group(i)
            if execcmd is not None:
                break
        assert (execcmd is not None)
        charbefore = match.group(1)
        subp = subprocess.run(execcmd, shell=True, stdout=subprocess.PIPE)
        result = str(subp.stdout, "utf-8")
        result = charbefore + trim_last_newline(result)

        replaced = self.execre.sub(result, line, count=1)
        return replaced
