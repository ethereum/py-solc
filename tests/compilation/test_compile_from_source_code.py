from solc import (
    get_solc_version,
    compile_source,
)


def test_source_code_compilation():
    SOURCE = "contract Foo { function Foo() {} function return13() returns (uint) { return 13; } }"
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
    assert foo_contract_data['meta']['compilerVersion'] == get_solc_version()
