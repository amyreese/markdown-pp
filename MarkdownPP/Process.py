# Copyright (C) 2010 John Reese
# Licensed under the MIT license


class Process:
	"""
	Framework for allowing modules to modify the input data as a set of transforms.
	"""
	
	data = []
	transforms = {}
	modules = []

	def register(self, module):
		self.modules.append(module)

	def input(self, file):
		self.data = file.readlines()

	def process(self):
		for module in self.modules:
			transforms = module.transform(self.data)
			transforms.sort(cmp=lambda x,y: cmp(x.linenum, y.linenum), reverse=True)

			for transform in transforms:
				linenum = transform.linenum

				if   transform.oper == "prepend":
					self.data[linenum:linenum] = transform.data

				elif transform.oper == "append":
					self.data[linenum+1:linenum+1] = transform.data

				elif transform.oper == "swap":
					self.data[linenum:linenum+1] = transform.data

				elif transform.oper == "drop":
					self.data[linenum:linenum+1] = []

				elif transform.oper == "noop":
					pass

	def output(self, file):
		linenum = 0
		for line in self.data:
			if not line is None:
				file.write(line)

			linenum += 1

