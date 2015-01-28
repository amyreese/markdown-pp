#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup

setup(name = "MarkdownPP",
      description = "Markdown preprocessor",
      version = "1.0",
      author = "John Reese",
      author_email = "john@noswap.com",
      url = "https://github.com/jreese/markdown-pp",
      classifiers=['License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Topic :: Utilities',
                   'Development Status :: 4 - Beta',
                   ],
      license='MIT License',
      scripts = ['markdown-pp.py'],
      packages = ['MarkdownPP', 'MarkdownPP/Modules'],
      )
