# Copyright (C) 2010 John Reese
# Licensed under the MIT license

import re
import httplib, urllib

from MarkdownPP.Module import Module
from MarkdownPP.Transform import Transform

blockre = re.compile("\$(\$?)..*\$(\$?)")
singlere = re.compile("\$(\$?)")

class LaTeXRender(Module):
	"""
	Module for rendering LaTeX enclosed between $ dollar signs $.
	Rendering is performed using QuickLaTeX via ProblemSetMarmoset.
	"""
	
	def render(self, formula):
		formula = formula.replace("$", "")
		encoded_formula = formula.replace("%","[comment]").replace("+","%2B")
		display_formula = formula.replace("\n","")
		
		params = urllib.urlencode({'engine': 'quicklatex', 'input': encoded_formula})
		headers = {"Content-type": "application/x-www-form-urlencoded",
		           "Accept": "text/plain"}
		conn = httplib.HTTPConnection("www.problemsetmarmoset.com")
		
		print params
		
		conn.request("POST", "/latex/render.php", params, headers)
		response = conn.getresponse()
		img_url = response.read()
		
		rendered_tex = '![{}]({})\n'.format(display_formula, img_url)
		return rendered_tex

	def transform(self, data):
		transforms = []
		linenum = 0
		in_block = False
		current_block = ""
		
		for line in data:
			if in_block:
				transforms.append(Transform(linenum, "drop"))
				current_block += "\n" + line
				
			match = blockre.search(line)
			if match:
				transforms.append(Transform(linenum, "swap", self.render(line)))
			else:
				match = singlere.search(line)
				if match:
					if in_block:
						transforms.pop() # undo last drop
						transforms.append(Transform(linenum, "swap", self.render(current_block)))
					else:
						current_block = line
						transforms.append(Transform(linenum, "drop"))
					in_block = not in_block
					
			linenum += 1

		return transforms
