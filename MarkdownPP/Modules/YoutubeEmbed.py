# Copyright (C) 2012 Alex Nisnevich
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import re
import os
import urllib
import logging

from MarkdownPP.Module import Module
from MarkdownPP.Transform import Transform

youtube_url_re = re.compile('^!VIDEO\s+"http://www\.youtube\.com'
                            '/embed/([a-zA-Z0-9\-]*)"')
glowfoto_server_re = re.compile("<uploadform>(.*)</uploadform>")
glowfoto_image_re = re.compile("<thumburl>(.*)</thumburl>")
codere = re.compile("^(    |\t)")
fencedcodere = re.compile("^```\w*$")

play_button_url = 'http://i.imgur.com/1IHylPh.png'


class YoutubeEmbed(Module):
    """
    Converts Youtube embed objects into links with screenshots,
    taken from Youtube.
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
                    processed_image_dir = os.path.join('images', 'youtube')
                    processed_image_path = os.path.join(processed_image_dir,
                                                        '%s.png' % url)

                    # do we already have a screenshot?
                    if not os.path.isfile(processed_image_path):
                        # try to add a play button to the screenshot
                        try:
                            import Image
                            from tempfile import NamedTemporaryFile

                            # create directories if needed
                            if not os.path.exists(processed_image_dir):
                                os.makedirs(processed_image_dir)

                            # create temporary files for image operations
                            screenshot_img = NamedTemporaryFile(suffix=".jpg")
                            button_img = NamedTemporaryFile(suffix=".png")

                            # grab screenshot and button image
                            urllib.urlretrieve(image_url, screenshot_img.name)
                            urllib.urlretrieve(play_button_url,
                                               button_img.name)

                            # layer the images using PIL and save
                            background = Image.open(screenshot_img.name)
                            foreground = Image.open(button_img.name)
                            background.paste(foreground, (90, 65), foreground)
                            background.save(processed_image_path)

                        except Exception as e:
                            logging.warning('Unable to add play button to '
                                            'YouTube screenshot (%s). Using '
                                            'the screenshot on its own '
                                            'instead.', e)

                    image_link = ('[![Link to Youtube video](%s)](%s)\n' %
                                  (processed_image_path, video_url))
                    transforms.append(Transform(linenum, "swap", image_link))

            linenum += 1

        return transforms
