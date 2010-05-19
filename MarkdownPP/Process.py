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
		linenum = 0
		for line in self.data:
			for module in self.modules:
				module.process(linenum, line)

			linenum += 1

		for module in self.modules:
			for transform in module.transforms():
				if transform.linenum not in self.transforms:
					self.transforms[transform.linenum] = []
				self.transforms[transform.linenum].append(transform)

	def output(self, file):
		linenum = 0
		for line in self.data:
			if linenum in self.transforms:
				for transform in self.transforms:

					if   transform.oper == "prepend":
						line = transform.data + line

					elif transform.oper == "append":
						line = line + transform.data

					elif transform.oper == "swap":
						line = transform.data

					elif transform.oper == "drop":
						line = None

					elif transform.oper == "noop":
						pass

			if not line is None:
				file.write(line)

			linenum += 1

			

