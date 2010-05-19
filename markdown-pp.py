#!/usr/bin/env python

# Copyright (C) 2010 John Reese
# Licensed under the MIT license

import sys
import MarkdownPP

if len(sys.argv) > 2:
	infile = sys.argv[1]
	outfile = sys.argv[2]
else:
	sys.exit(1)

mdpp = open(infile, "r")
md = open(outfile, "w")
	
MarkdownPP.MarkdownPP(input=mdpp, output=md, modules=MarkdownPP.modules.keys())

