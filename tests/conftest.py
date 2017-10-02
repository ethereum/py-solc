import pytest

import textwrap

from semantic_version import Spec

from solc import get_solc_version
from solc.main import solc_supports_standard_json_interface


@pytest.fixture()
def contracts_dir(tmpdir):
    return str(tmpdir.mkdir("contracts"))


@pytest.fixture(scope="session")
def solc_version():
    return get_solc_version()


@pytest.fixture()
def supported_solc_version(solc_version):
    if solc_version not in Spec('>=0.4.1,<=0.4.17,!=0.4.10,!=0.4.3,!=0.4.4,!=0.4.5'):
        raise AssertionError("Unsupported compiler version: {0}".format(solc_version))

    return solc_version


@pytest.fixture()
def is_new_key_format():
    return get_solc_version() in Spec('>=0.4.9')


@pytest.fixture()
def FOO_SOURCE(supported_solc_version, solc_version):
    if solc_version in Spec('<0.4.17'):
        return textwrap.dedent('''\
            pragma solidity ^0.4.0;

            contract Foo {
                function Foo() {}

                function return13() public returns (uint) {
                    return 13;
                }
            }
            ''')
    else:
        return textwrap.dedent('''\
            pragma solidity ^0.4.17;

            contract Foo {
                function Foo() public {}

                function return13() public pure returns (uint) {
                    return 13;
                }
            }
            ''')


@pytest.fixture()
def BAR_SOURCE(supported_solc_version):
    return textwrap.dedent('''\
        pragma solidity ^0.4.0;

        contract Bar {
            function Bar() public {}
        }
        ''')


@pytest.fixture()
def BAZ_SOURCE(supported_solc_version):
    return textwrap.dedent('''\
        pragma solidity ^0.4.0;

        import "contracts/Bar.sol";

        contract Baz is Bar {
            function Baz() public {}

            function get_funky() public returns (string) {
                return "funky";
            }
        }
        ''')


@pytest.fixture()
def INVALID_SOURCE(supported_solc_version):
    return textwrap.dedent('''\
        pragma solidity ^0.4.0;
        contract Foo {
        ''')


def pytest_runtest_setup(item):
    if (item.get_marker('requires_standard_json') is not None and
        not solc_supports_standard_json_interface()):
        pytest.skip('requires `--standard-json` support')
