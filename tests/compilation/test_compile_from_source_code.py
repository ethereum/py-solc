import pytest

from solc import compile_source

pytestmark = pytest.mark.usefixtures('supported_solc_version')


def test_source_code_compilation(FOO_SOURCE, is_new_key_format):
    output = compile_source(FOO_SOURCE, optimize=True)
    assert output

    if is_new_key_format:
        contact_key = '<stdin>:Foo'
    else:
        contact_key = 'Foo'

    assert contact_key in output

    foo_contract_data = output[contact_key]
    assert 'bin' in foo_contract_data
    assert 'bin-runtime' in foo_contract_data
