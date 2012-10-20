#!/usr/bin/env python
# -*- coding: utf-8 -*-


from distutils.core import setup

setup(name = "MarkdownPP",
      version = "1.0",
      description = "Markdown",
      author = "John Reese",
      author_email = "john@noswap.com",
      url = "https://github.com/jreese/markdown-pp.git",
      data_files = [('/usr/local/bin', ['markdown-pp.py'])], 
      packages = ['MarkdownPP', 'MarkdownPP/Modules'],)
