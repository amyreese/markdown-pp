# Copyright (C) 2010 John Reese
# Licensed under the MIT license

import re
import httplib, urllib

from MarkdownPP.Module import Module
from MarkdownPP.Transform import Transform

singlelinere = re.compile("\$(\$?)..*\$(\$?)") # $...$ (or $$...$$)
startorendre = re.compile("^\$(\$?)|^\S.*\$(\$?)$") # $... or ...$ (or $$... or ...$$)
codere = re.compile("^(    |\t)")
fencedcodere = re.compile("^```\w*$")

class LaTeXRender(Module):
	"""
	Module for rendering LaTeX enclosed between $ dollar signs $.
	Rendering is performed using QuickLaTeX via ProblemSetMarmoset.
	"""
	
	def render(self, formula):
		formula = formula.replace("$", "")
		encoded_formula = formula.replace("%","[comment]").replace("+","%2B")
		display_formula = formula.replace("\n","")
		print 'Rendering: %s ...' % display_formula
		
		params = urllib.urlencode({'engine': 'quicklatex', 'input': encoded_formula})
		headers = {"Content-type": "application/x-www-form-urlencoded",
		           "Accept": "text/plain"}
		conn = httplib.HTTPConnection("www.problemsetmarmoset.com")
		
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
		in_fenced_code_block = False
		
		for line in data:
			# Fenced code blocks (Github-flavored markdown)
			match = fencedcodere.search(line)
			if match:
				if in_fenced_code_block:
					in_fenced_code_block = False
				else:
					in_fenced_code_block = True
			
			is_code_block = codere.search(line)
			if not in_fenced_code_block and not is_code_block:
				if in_block:
					transforms.append(Transform(linenum, "drop"))
					current_block += "\n" + line
					
				match = singlelinere.search(line)
				if match:
					tex = match.group(0)
					before_tex = line[0:line.find(tex)]
					after_tex = line[(line.find(tex) + len(tex)) : len(line)]
					transforms.append(Transform(linenum, "swap", before_tex + self.render(tex) + after_tex))
				else:
					match = startorendre.search(line)
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
