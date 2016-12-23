import os

from solc import (
    get_solc_version,
    compile_files,
)


def test_remappings(contracts_dir):
    IMPORT_SOURCE = "contract Bar {}"
    SOURCE = 'import "bar/moo.sol"; contract Foo is Bar { function Foo() {} function return13() returns (uint) { return 13; } }'

    baz_path = os.path.abspath(os.path.join(contracts_dir, "baz"))
    os.makedirs(baz_path)

    source_file_path = os.path.join(baz_path, 'Moo.sol')
    with open(source_file_path, 'w') as source_file:
        source_file.write(IMPORT_SOURCE)

    source_file_path = os.path.join(contracts_dir, 'Foo.sol')
    with open(source_file_path, 'w') as source_file:
        source_file.write(SOURCE)

    output = compile_files([source_file_path], remappings=["bar={}".format(baz_path)])

    assert output
    assert 'Foo' in output
