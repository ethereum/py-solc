import os

import pytest

from solc import (
    compile_standard,
)
from solc.exceptions import SolcError

pytestmark = pytest.mark.requires_standard_json


def contract_in_output_map(contract_name, contract_map):
    try:
        return int(contract_map
            ['contracts/{}.sol'.format(contract_name)]
            [contract_name]
            ['evm']['bytecode']['object'], 16) is not None
    except:
        return False


def test_compile_standard(FOO_SOURCE):
    result = compile_standard({
        'language': 'Solidity',
        'sources': {
            'contracts/Foo.sol': {
                'content': FOO_SOURCE,
            },
        },
        'outputSelection': {
            "*": {"*": ["evm.bytecode.object"]},
        },
    })

    assert isinstance(result, dict)
    assert 'contracts' in result
    assert contract_in_output_map('Foo', result['contracts'])


def test_compile_standard_invalid_source(INVALID_SOURCE):
    with pytest.raises(SolcError):
        compile_standard({
            'language': 'Solidity',
            'sources': {
                'contracts/Foo.sol': {
                    'content': INVALID_SOURCE,
                },
            },
            'outputSelection': {
                "*": {"*": ["evm.bytecode.object"]},
            },
        })


def test_compile_standard_with_dependency(BAR_SOURCE, BAZ_SOURCE):
    result = compile_standard({
        'language': 'Solidity',
        'sources': {
            'contracts/Bar.sol': {
                'content': BAR_SOURCE,
            },
            'contracts/Baz.sol': {
                'content': BAZ_SOURCE,
            },
        },
        'outputSelection': {
            "*": {"*": ["evm.bytecode.object"]},
        },
    })

    assert isinstance(result, dict)
    assert 'contracts' in result
    assert contract_in_output_map('Bar', result['contracts'])
    assert contract_in_output_map('Baz', result['contracts'])


def test_compile_standard_with_file_paths(FOO_SOURCE, is_new_key_format, contracts_dir):
    source_file_path = os.path.join(contracts_dir, 'Foo.sol')
    with open(source_file_path, 'w') as source_file:
        source_file.write(FOO_SOURCE)

    result = compile_standard({
        'language': 'Solidity',
        'sources': {
            'contracts/Foo.sol': {
                'urls': [source_file_path],
            },
        },
        'outputSelection': {
            "*": {"*": ["evm.bytecode.object"]},
        },
    }, allow_paths=contracts_dir)

    assert isinstance(result, dict)
    assert 'contracts' in result
    assert contract_in_output_map('Foo', result['contracts'])
