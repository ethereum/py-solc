import pytest

import os

from semantic_version import Spec
from solc import (
    get_solc_version,
    compile_files,
)

pytestmark = pytest.mark.usefixtures('supported_solc_version')


def test_source_files_compilation(FOO_SOURCE, is_new_key_format, contracts_dir):
    source_file_path = os.path.join(contracts_dir, 'Foo.sol')
    with open(source_file_path, 'w') as source_file:
        source_file.write(FOO_SOURCE)

    output = compile_files([source_file_path], optimize=True)

    assert output

    if is_new_key_format:
        contract_key = '{0}:Foo'.format(os.path.abspath(source_file_path))
    else:
        contract_key = 'Foo'

    assert contract_key in output

    foo_contract_data = output[contract_key]
    assert 'bin' in foo_contract_data
    assert 'bin-runtime' in foo_contract_data
