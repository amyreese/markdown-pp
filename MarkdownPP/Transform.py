# Copyright (C) 2010 John Reese
# Licensed under the MIT license

class Transform:
	"""
	This class represents a single modification to the data set, designed
	to be applied in descending order by line number.  The operation determines
	where the new data will be applied, and how.
	"""

	lineum = -1
	oper = "noop"
	data = ""

