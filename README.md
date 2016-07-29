# py-solc

[![Build Status](https://travis-ci.org/pipermerriam/py-solc.png)](https://travis-ci.org/pipermerriam/py-solc)
[![PyPi version](https://pypip.in/v/py-solc/badge.png)](https://pypi.python.org/pypi/py-solc)
[![PyPi downloads](https://pypip.in/d/py-solc/badge.png)](https://pypi.python.org/pypi/py-solc)
   

Python wrapper around the `solc` Solidity compiler.


# Dependency

This library requires the `solc` executable to be present.

solc 0.3.5 or newer is required. [solc installation instructions](http://solidity.readthedocs.io/en/latest/installing-solidity.html)


# Quickstart

Installation

```sh
pip install py-solc
```

```python
>>> from solc import compile_source, compile_files, link_code
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
>>> unlinked_code = "606060405260768060106000396000f3606060405260e060020a6000350463e7f09e058114601a575b005b60187f0c55699c00000000000000000000000000000000000000000000000000000000606090815273__TestA_________________________________90630c55699c906064906000906004818660325a03f41560025750505056"
>>> link_code(unlinked_code, {'TestA': '0xd3cda913deb6f67967b99d67acdfa1712c293601'})
... "606060405260768060106000396000f3606060405260e060020a6000350463e7f09e058114601a575b005b60187f0c55699c00000000000000000000000000000000000000000000000000000000606090815273d3cda913deb6f67967b99d67acdfa1712c29360190630c55699c906064906000906004818660325a03f41560025750505056"
```
