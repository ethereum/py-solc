import pytest

from solc import (
    compile_standard,
)
from solc.exceptions import SolcError

pytestmark = pytest.mark.requires_standard_json


def test_compile_standard(FOO_SOURCE):
    result = compile_standard({
        'language': 'Solidity',
        'sources': {
            'Foo.sol': {
                'content': FOO_SOURCE,
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


def test_compile_standard_invalid_source(INVALID_SOURCE):
    with pytest.raises(SolcError):
        compile_standard({
            'language': 'Solidity',
            'sources': {
                'Foo.sol': {
                    'content': INVALID_SOURCE,
                },
            },
            'outputSelection': {
                "*": {"*": ["evm.bytecode.object"]},
            },
        })
