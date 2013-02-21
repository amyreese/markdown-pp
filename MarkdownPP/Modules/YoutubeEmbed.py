# Copyright (C) 2012 Alex Nisnevich
# Licensed under the MIT license

import re
import httplib, urllib

from MarkdownPP.Module import Module
from MarkdownPP.Transform import Transform

youtube_url_re = re.compile("<iframe.*http://www\.youtube\.com/embed/([a-zA-Z0-9\-]*)['\"].*</iframe>")
glowfoto_server_re = re.compile("<uploadform>(.*)</uploadform>")
glowfoto_image_re = re.compile("<thumburl>(.*)</thumburl>")
codere = re.compile("^(    |\t)")
fencedcodere = re.compile("^```\w*$")

play_button_url = 'http://i.imgur.com/1IHylPh.png'

class YoutubeEmbed(Module):
	"""
	Converts Youtube embed objects into links with screenshots, taken from Youtube.
	"""

	def transform(self, data):
		transforms = []
		in_fenced_code_block = False
		linenum = 0

		for line in data:
			# Handling fenced code blocks (for Github-flavored markdown)
			if fencedcodere.search(line):
				if in_fenced_code_block:
					in_fenced_code_block = False
				else:
					in_fenced_code_block = True

			# Are we in a code block?
			if not in_fenced_code_block and not codere.search(line):
				match = youtube_url_re.search(line)
				if match:
					# find URL of youtube video and screenshot
					url = match.group(1)
					image_url = 'http://img.youtube.com/vi/%s/0.jpg' % url
					video_url = 'http://www.youtube.com/watch?v=%s' % url

					# try to add a play button to the screenshot
					try:
						import tempfile
						import Image
						import requests

						# create temporary files for image operations
						screenshot_img = tempfile.NamedTemporaryFile(suffix=".jpg")
						button_img = tempfile.NamedTemporaryFile(suffix=".png")
						final_img = tempfile.NamedTemporaryFile(suffix=".png")

						# grab screenshot and button image
						urllib.urlretrieve(image_url, screenshot_img.name)
						urllib.urlretrieve(play_button_url, button_img.name)

						# layer the images using PIL
						background = Image.open(screenshot_img.name)
						foreground = Image.open(button_img.name)
						background.paste(foreground, (90, 65), foreground)
						background.save(final_img.name)

						# upload resulting image to glowfoto (no api key required)
						r = requests.get('http://www.glowfoto.com/getserverxml.php')
						match = glowfoto_server_re.search(r.text)
						if match:
							post_url = match.group(1)
							r = requests.post(post_url, files={'image': open(final_img.name, 'rb')})
							match = glowfoto_image_re.search(r.text)
							if match:
								image_url = match.group(1).replace('T.png', 'L.png').encode('ascii','ignore')
					except Exception, e:
						print 'Unable to add play button to YouTube screenshot (%s). Using the screenshot on its own instead.' % e
						pass

					image_link = '[![Link to Youtube video](%s)](%s)\n' % (image_url, video_url)
					transforms.append(Transform(linenum, "swap", image_link))

			linenum += 1

		return transforms
