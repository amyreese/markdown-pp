# Copyright 2015 John Reese
# Licensed under the MIT license

import os
from os import path

modules = {}

def load_modules():
	dirname = path.dirname(path.abspath(__file__))
	filenames = os.listdir(dirname)

	for filename in os.listdir(dirname):
		(modulename, extension) = path.splitext(filename)
		if extension.lower() == ".py" and modulename.lower() != "__init__":
			module = __import__("MarkdownPP.Modules.%s" % modulename, fromlist=[modulename])
			if modulename in dir(module):
				nickname = modulename.lower()
				modules[nickname] = module.__dict__[modulename]

load_modules()

