from __future__ import unicode_literals

import pytest

import json
import os

from solc import get_solc_version
from solc.wrapper import (
    solc_wrapper,
)


def is_benign(err):
    return not err or err in (
        'Warning: This is a pre-release compiler version, please do not use it in production.\n',
    )


def test_help():
    output, err, _, _ = solc_wrapper(help=True, success_return_code=1)
    assert output
    assert 'Solidity' in output
    assert is_benign(err)


def test_version():
    output, err, _, _ = solc_wrapper(version=True)
    assert output
    assert 'Version' in output
    assert is_benign(err)


def test_providing_stdin(FOO_SOURCE):
    output, err, _, _ = solc_wrapper(stdin=FOO_SOURCE, bin=True)
    assert output
    assert 'Foo' in output
    assert is_benign(err)


def test_providing_single_source_file(contracts_dir, FOO_SOURCE):
    source_file_path = os.path.join(contracts_dir, 'Foo.sol')
    with open(source_file_path, 'w') as source_file:
        source_file.write(FOO_SOURCE)

    output, err, _, _ = solc_wrapper(source_files=[source_file_path], bin=True)
    assert output
    assert 'Foo' in output
    assert is_benign(err)


def test_providing_multiple_source_files(contracts_dir, FOO_SOURCE, BAR_SOURCE):
    source_file_a_path = os.path.join(contracts_dir, 'Foo.sol')
    source_file_b_path = os.path.join(contracts_dir, 'Bar.sol')

    with open(source_file_a_path, 'w') as source_file:
        source_file.write(FOO_SOURCE)
    with open(source_file_b_path, 'w') as source_file:
        source_file.write(BAR_SOURCE)

    output, err, _, _ = solc_wrapper(source_files=[source_file_a_path, source_file_b_path], bin=True)
    assert output
    assert 'Foo' in output
    assert 'Bar' in output
    assert is_benign(err)


@pytest.mark.requires_standard_json
def test_providing_standard_json_input(FOO_SOURCE, BAR_SOURCE):
    stdin = json.dumps({
        "language": "Solidity",
        "sources": {
            "Foo.sol": {
              "content": FOO_SOURCE
            },
            "Bar.sol": {
              "content": BAR_SOURCE
            }
        },
        "settings":
        {
            "outputSelection": {
              "*": {
                "*": [ "abi", "evm.bytecode.link_references", "evm.bytecode.object", "devdoc", "metadata", "userdoc" ]
              }
            }
        }
    })

    output, err, _, _ = solc_wrapper(stdin=stdin, standard_json=True)
    output = json.loads(output)
    assert output
    assert 'Foo.sol' in output['contracts']
    assert 'Bar.sol' in output['contracts']
    assert is_benign(err)
