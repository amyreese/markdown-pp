# Copyright (C) 2010 John Reese
# Licensed under the MIT license

from Transform import Transform

class Module:
	"""
	This class provides a generic interface for the preprocessor to pass
	data to the module and retrieve a list of Transforms to the data.
	"""

	def transform(self, data):
		"""
		This method should generate a list of Transform objects for each
		modification to the original data, and return this list when ready.
		"""

		return []

