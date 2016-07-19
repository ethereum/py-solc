import os

from solc.wrapper import (
    solc_wrapper,
)


def test_help():
    output, err = solc_wrapper(help=True, success_return_code=1)
    assert output
    assert 'Solidity' in output
    assert not err


def test_version():
    output, err = solc_wrapper(version=True)
    assert output
    assert 'Version' in output
    assert not err


def test_providing_stdin():
    stdin_bytes = b"contract Foo { function Foo() {} }"
    output, err = solc_wrapper(stdin_bytes=stdin_bytes, bin=True)
    assert output
    assert 'Foo' in output
    assert not err


def test_providing_single_source_file(contracts_dir):
    source_file_path = os.path.join(contracts_dir, 'Foo.sol')
    with open(source_file_path, 'w') as source_file:
        source_file.write("contract Foo { function Foo() {} }")

    output, err = solc_wrapper(source_files=[source_file_path], bin=True)
    assert output
    assert 'Foo' in output
    assert not err


def test_providing_multiple_source_files(contracts_dir):
    source_file_a_path = os.path.join(contracts_dir, 'Foo.sol')
    source_file_b_path = os.path.join(contracts_dir, 'Bar.sol')

    with open(source_file_a_path, 'w') as source_file:
        source_file.write("contract Foo { function Foo() {} }")
    with open(source_file_b_path, 'w') as source_file:
        source_file.write("contract Bar { function Bar() {} }")

    output, err = solc_wrapper(source_files=[source_file_a_path, source_file_b_path], bin=True)
    assert output
    assert 'Foo' in output
    assert 'Bar' in output
    assert not err
