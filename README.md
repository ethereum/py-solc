# py-solc

[![Build Status](https://travis-ci.org/pipermerriam/py-solc.png)](https://travis-ci.org/pipermerriam/py-solc)
[![PyPi version](https://pypip.in/v/py-solc/badge.png)](https://pypi.python.org/pypi/py-solc)
[![PyPi downloads](https://pypip.in/d/py-solc/badge.png)](https://pypi.python.org/pypi/py-solc)
   

Python wrapper around the `solc` solidity compiler.


# Dependency

This library requires the `solc` executable to be present.


# Quickstart

Installation

```sh
pip install py-solc
```

```python
>>> from solc import compile_source, compile_files
>>> compile_source("contract Foo { function Foo() {} }")
{
    'Foo': {
        'abi': [{'inputs': [], 'type': 'constructor'}],
        'code': '0x60606040525b5b600a8060126000396000f360606040526008565b00',
        'code_runtime': '0x60606040526008565b00',
        'source': None,
        'meta': {
            'compilerVersion': '0.3.5-9da08ac3',
            'language': 'Solidity',
            'languageVersion': '0',
        },
    },
}
>>> compile_files(["/path/to/Foo.sol", "/path/to/Bar.sol"])
{
    'Foo': {
        'abi': [{'inputs': [], 'type': 'constructor'}],
        'code': '0x60606040525b5b600a8060126000396000f360606040526008565b00',
        'code_runtime': '0x60606040526008565b00',
        'source': None,
        'meta': {
            'compilerVersion': '0.3.5-9da08ac3',
            'language': 'Solidity',
            'languageVersion': '0',
        },
    },
    'Bar': {
        'abi': [{'inputs': [], 'type': 'constructor'}],
        'code': '0x60606040525b5b600a8060126000396000f360606040526008565b00',
        'code_runtime': '0x60606040526008565b00',
        'source': None,
        'meta': {
            'compilerVersion': '0.3.5-9da08ac3',
            'language': 'Solidity',
            'languageVersion': '0',
        },
    },
}
```
