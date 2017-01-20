#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

from os import path
import shutil

if path.isfile('README.md'):
    shutil.copyfile('README.md', 'README')

setup(
    name='MarkdownPP',
    description='Markdown preprocessor',
    version='1.3',
    author='John Reese',
    author_email='john@noswap.com',
    url='https://github.com/jreese/markdown-pp',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
        'Development Status :: 4 - Beta',
    ],
    license='MIT License',
    packages=['MarkdownPP', 'MarkdownPP/Modules'],
    entry_points={
        'console_scripts': [
            'markdown-pp = MarkdownPP.main:main'
        ],
    },
    install_requires=[
        'Watchdog >= 0.8.3',
    ],
)
