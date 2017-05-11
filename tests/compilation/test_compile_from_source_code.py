import pytest

from solc import compile_source

pytestmark = pytest.mark.usefixtures('supported_solc_version')


def test_source_code_compilation(is_new_key_format):
    SOURCE = "pragma solidity ^0.4.0;\ncontract Foo { function Foo() {} function return13() returns (uint) { return 13; } }"

    output = compile_source(SOURCE, optimize=True)
    assert output

    if is_new_key_format:
        contact_key = '<stdin>:Foo'
    else:
        contact_key = 'Foo'

    assert contact_key in output

    foo_contract_data = output[contact_key]
    assert 'bin' in foo_contract_data
    assert 'bin-runtime' in foo_contract_data
