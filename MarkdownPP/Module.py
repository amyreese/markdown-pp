# Copyright (C) 2010 John Reese
# Licensed under the MIT license

from Transform import Transform

class Module:

	def transform(self, data):
		tform = Transform()
		tform.linenum = 3
		tform.oper = "swap"
		tform.data = "TIC TOC"

		return [tform]
