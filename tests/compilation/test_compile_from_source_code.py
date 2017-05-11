from semantic_version import Spec
from solc import (
    get_solc_version,
    compile_source,
)
from ..test_utils import checks_solc_version


@checks_solc_version
def test_source_code_compilation():
    SOURCE = "pragma solidity ^0.4.0;\ncontract Foo { function Foo() {} function return13() returns (uint) { return 13; } }"

    output = compile_source(SOURCE, optimize=True)
    assert output

    if get_solc_version() in Spec('>=0.4.9'):
        contact_key = '<stdin>:Foo'
    else:
        contact_key = 'Foo'

    assert contact_key in output

    foo_contract_data = output[contact_key]
    assert 'bin' in foo_contract_data
    assert 'bin-runtime' in foo_contract_data
