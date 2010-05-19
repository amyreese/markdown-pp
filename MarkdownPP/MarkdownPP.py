# Copyright (C) 2010 John Reese
# Licensed under the MIT license

from Processor import Processor
import Modules

class MarkdownPP:
	"""
	Simplified front-end interface for the Processor and Module systems.
	Takes input and output file names or objects, and a list of module names.
	Automatically executes the preprocessor with the requested modules.
	"""

	def __init__(self, input=None, output=None, modules=None):
		pp = Processor()

		map(str.lower, modules)

		for name in modules:
			if Modules.modules.has_key(name):
				module = Modules.modules[name]()
				pp.register(module)

		pp.input(input)
		pp.process()
		pp.output(output)

