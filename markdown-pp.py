#!/usr/bin/env python2

# Copyright (C) 2010 John Reese
# Licensed under the MIT license

import sys
import MarkdownPP

if len(sys.argv) > 2:
	mdpp = open(sys.argv[1], "r")
	md = open(sys.argv[2], "w")

elif len(sys.argv) > 1:
	mdpp = open(sys.argv[1], "r")
	md = sys.stdout

else:
	sys.exit(1)
	
MarkdownPP.MarkdownPP(input=mdpp, output=md, modules=MarkdownPP.modules.keys())

mdpp.close()
md.close()
