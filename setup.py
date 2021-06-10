#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

requirements = [
    'markdown',
    'beautifulsoup4',
    'lxml'
]

setup(
    name='markdown-macros',
    version='0.1.0',
    description='A Python-Markdown extension that defines a markup for including macros in the markdown text',
    author='Anand Chitipothu',
    author_email='anand@fossunited.org',
    url='https://github.com/fossunited/markdown-macros',
    py_modules=[
        'markdown_macros',
    ],
    install_requires=requirements,
    license="MIT",
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        "markdown.extensions": [
            "macros = markdown_macros:MacroExtension"
        ]
    },
)
