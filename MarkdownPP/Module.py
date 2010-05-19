# Copyright (C) 2010 John Reese
# Licensed under the MIT license

from Transform import Transform

class Module:

	toc = -1

	def process(self, linenum, line):
		if line == "!TOC":
			self.toc = linenum

	def transforms(self):
		tform = Transform()
		tform.linenum = self.toc
		tform.oper = "swap"
		tform.data = "TIC TOC"

		return [tform]
