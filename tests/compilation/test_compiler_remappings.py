import os

from semantic_version import Spec
from solc import (
    get_solc_version,
    compile_files,
)


def test_import_remapping(contracts_dir):
    IMPORT_SOURCE = "contract Bar {}"
    SOURCE = 'import "bar/Moo.sol"; contract Foo is Bar { function Foo() {} function return13() returns (uint) { return 13; } }'

    solc_version = get_solc_version()

    baz_path = os.path.abspath(os.path.join(contracts_dir, "baz"))
    os.makedirs(baz_path)

    source_file_path = os.path.join(baz_path, 'Moo.sol')
    with open(source_file_path, 'w') as source_file:
        source_file.write(IMPORT_SOURCE)

    source_file_path = os.path.join(contracts_dir, 'Foo.sol')
    with open(source_file_path, 'w') as source_file:
        source_file.write(SOURCE)

    output = compile_files([source_file_path], import_remappings=["bar={}".format(baz_path)])

    assert output

    if solc_version in Spec('>=0.4.9'):
        contact_key = '{0}:Foo'.format(os.path.abspath(source_file_path))
    else:
        contact_key = 'Foo'

    assert contact_key in output
