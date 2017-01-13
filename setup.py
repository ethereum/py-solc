#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import (
    setup,
    find_packages,
)


DIR = os.path.dirname(os.path.abspath(__file__))

readme = open(os.path.join(DIR, 'README.md')).read()


setup(
    name='py-solc',
    version="1.0.0",
    description="""Python wrapper around the solc binary""",
    long_description=readme,
    author='Piper Merriam',
    author_email='pipermerriam@gmail.com',
    url='https://github.com/pipermerriam/py-solc',
    include_package_data=True,
    py_modules=['solc'],
    extras_require={
        'gevent': [
            "gevent>=1.1.1,<1.2.0",
        ],
    },
    license="MIT",
    zip_safe=False,
    keywords='ethereum solidity solc',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
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
