#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    setup,
    find_packages,
)


setup(
    name='py-solc',
    # *IMPORTANT*: Don't manually change the version here. Use the 'bumpversion' utility.
    version='3.0.0',
    description="""Python wrapper around the solc binary""",
    long_description_markdown_filename='README.md',
    author='Piper Merriam',
    author_email='pipermerriam@gmail.com',
    url='https://github.com/ethereum/py-solc',
    include_package_data=True,
    py_modules=['solc'],
    setup_requires=['setuptools-markdown'],
    python_requires='>=3.4, <4',
    install_requires=[
        "semantic_version>=2.6.0",
    ],
    license="MIT",
    zip_safe=False,
    keywords='ethereum solidity solc',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
