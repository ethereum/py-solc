from solc import (
    get_solc_version,
    get_solc_version_string,
    compile_source,
)


def test_source_code_compilation():
    solc_version_string = get_solc_version_string()

    solc_version = get_solc_version()

    if solc_version == "0.4.1":
        SOURCE = "pragma solidity 0.4.1;\ncontract Foo { function Foo() {} function return13() returns (uint) { return 13; } }"
    elif solc_version == "0.3.6":
        SOURCE = "contract Foo { function Foo() {} function return13() returns (uint) { return 13; } }"
    else:
        raise AssertionError("Unsupported compiler version")


    output = compile_source(SOURCE)
    assert output
    assert 'Foo' in output

    foo_contract_data = output['Foo']
    assert 'code' in foo_contract_data
    assert 'code_runtime' in foo_contract_data
    assert 'source' in foo_contract_data
    assert 'meta' in foo_contract_data
    assert 'compilerVersion' in foo_contract_data['meta']

    # TODO: figure out how to include source.
    assert foo_contract_data['source'] is None
    assert foo_contract_data['meta']['compilerVersion'] == solc_version_string
