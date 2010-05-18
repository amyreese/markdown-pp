#!/usr/bin/env python

# Copyright (C) 2010 John Reese
# Licensed under the MIT license

from os import path
import re
import sys

tocre = re.compile("!TOC")
atxre = re.compile("^(#+)\s*(.+)$")  
setextre = re.compile("^(=+|-+)\s*$")

class MarkdownPPHeader:
	depth = 0
	title = ""
	section = ""

	def __init__(self, depth, title):
		self.depth = depth
		self.title = title
		self.id = re.sub("(\s+)", "", title).lower()

	def __str__(self):
		return "Header(depth: %d, id: %s)" % (self.depth, self.id)

	def __unicode__(self):
		return self.__str__()

class MarkdownPPStatus:
	input = []
	toclines = []
	headers = {}
	toc = ""
	
	def __init__(self, file):
		self.input = file.readlines()

	def process(self):
		lastline = None
		linenum = 0

		tocfound = False
		lowestdepth = 10
		for line in self.input:
			match = tocre.search(line)
			if match:
				tocfound = True
				continue

			if tocfound:
				depth = lowestdepth

				match = atxre.search(line)
				if match:
					depth = len(match.group(1))

				match = setextre.search(line)
				if match:
					depth = 1 if match.group(1)[0] == "=" else 2

				if depth < lowestdepth:
					lowestdepth = depth

		depthoffset = 1 - lowestdepth

		for line in self.input:
			match = tocre.search(line)
			if match:
				self.toclines.append(linenum)

			match = atxre.search(line)
			if match:
				depth = len(match.group(1)) + depthoffset
				title = match.group(2)
				self.headers[linenum] = MarkdownPPHeader(depth, title)

			match = setextre.search(line)
			if match:
				depth = 1 if match.group(1)[0] == "=" else 2
				depth += depthoffset
				title = lastline.strip()
				self.headers[linenum-1] = MarkdownPPHeader(depth, title)

			lastline = line
			linenum += 1

		keys = self.headers.keys()
		keys.sort()

		stack = []
		headernum = 0
		lastdepth = 1
		for linenum in keys:
			header = self.headers[linenum]

			if linenum < self.toclines[0]:
				continue

			while header.depth > lastdepth:
				stack.append(headernum)
				headernum = 0
				lastdepth += 1

			while header.depth < lastdepth:
				headernum = stack.pop()
				lastdepth -= 1

			headernum += 1

			if header.depth == 1:
				header.section = "%d\\. " % headernum
			else:
				header.section = ".".join([str(x) for x in stack]) + ".%d\\. " % headernum

			self.toc += "%s [%s](#%s)  \n" % (header.section, header.title, header.id)
			self.input[linenum] = re.sub(header.title, header.section + header.title, self.input[linenum])

	def __str__(self):
		return "MarkdownPPStatus: \n\ttoclines: %s\n\theaders: %s" % (str(self.toclines), str(self.headers))

	def __unicode__(self):
		return self.__str__()

class MarkdownPP:
	"""
	Creates an object to pre-process a Markdown styled file for some simple
	optimizations and automations.
	"""

	def __init__(self):
		pass

	def read(self, file):
		"""
		Does the initial reading pass of a Markdown file object opened for reading
		"""

		status = MarkdownPPStatus(file)

		return status

	def write(self, status, file):
		"""
		Writes out the final pre-processed Markdown code to a file object opened for writing
		"""

		linenum = 0
		for line in status.input:
			if status.headers.has_key(linenum):
				header = status.headers[linenum]
				file.write("<a name=\"%s\"/>\n" % header.id) 

			if linenum in status.toclines:
				file.write(status.toc)
				line = ""

			file.write(line)
			linenum += 1

	def generate(self, filename, output=None):
		"""
		Helper method for automating the read/preprocess/write cycle
		"""

		if path.isfile(filename):
			status = self.read(open(filename, "r"))
		else:
			sys.exit(3)

		status.process()

		if output is None:
			root, ext = path.splitext(filename)
			ofile = open(root + ".md", "w")
			self.write(status, ofile)
			ofile.close()
		else:
			self.write(status, output)

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		sys.exit(1)

	mdpp = MarkdownPP()
	mdpp.generate(filename)
