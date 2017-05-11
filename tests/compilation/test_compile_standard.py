import pytest

import textwrap

from solc import (
    compile_standard,
)
from solc.exceptions import SolcError

from ..test_utils import skipif_no_standard_json


@skipif_no_standard_json
def test_compile_standard():
    result = compile_standard({
        'language': 'Solidity',
        'sources': {
            'Foo.sol': {
                'content': textwrap.dedent('''\
                    pragma solidity ^0.4.0;
                    contract Foo {
                        function Foo() {}
                        function return13() returns (uint) {
                            return 13;
                        }
                    }'''),
            },
        },
        'outputSelection': {
            "*": {"*": ["evm.bytecode.object"]},
        },
    })

    assert isinstance(result, dict)
    assert 'contracts' in result
    assert 'Foo.sol' in result['contracts']
    assert 'Foo' in result['contracts']['Foo.sol']
    assert 'evm' in result['contracts']['Foo.sol']['Foo']
    assert 'bytecode' in result['contracts']['Foo.sol']['Foo']['evm']
    assert 'object' in result['contracts']['Foo.sol']['Foo']['evm']['bytecode']
    int(result['contracts']['Foo.sol']['Foo']['evm']['bytecode']['object'], 16)


@skipif_no_standard_json
def test_compile_standard_invalid_source():
    with pytest.raises(SolcError):
        compile_standard({
            'language': 'Solidity',
            'sources': {
                'Foo.sol': {
                    'content': textwrap.dedent('''\
                        pragma solidity ^0.4.0;
                        contract Foo {'''),
                },
            },
            'outputSelection': {
                "*": {"*": ["evm.bytecode.object"]},
            },
        })