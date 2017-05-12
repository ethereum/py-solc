import os

from semantic_version import Spec
from solc import (
    get_solc_version,
    compile_files,
)


def test_import_remapping(contracts_dir, is_new_key_format, BAR_SOURCE, BAZ_SOURCE):
    solc_version = get_solc_version()

    source_file_path = os.path.join(contracts_dir, 'Bar.sol')
    with open(source_file_path, 'w') as source_file:
        source_file.write(BAR_SOURCE)

    source_file_path = os.path.join(contracts_dir, 'Baz.sol')
    with open(source_file_path, 'w') as source_file:
        source_file.write(BAZ_SOURCE)

    output = compile_files([source_file_path], import_remappings=["contracts={}".format(contracts_dir)])

    assert output

    if is_new_key_format:
        contact_key = '{0}:Baz'.format(os.path.abspath(source_file_path))
    else:
        contact_key = 'Baz'

    assert contact_key in output
