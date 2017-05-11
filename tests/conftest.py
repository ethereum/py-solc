import pytest

from semantic_version import Spec

from solc import get_solc_version
from solc.main import solc_supports_standard_json_interface


@pytest.fixture()
def contracts_dir(tmpdir):
    return str(tmpdir.mkdir("contracts"))


@pytest.fixture()
def supported_solc_version():
    solc_version = get_solc_version()
    if solc_version not in Spec('>=0.4.1,<=0.4.11'):
        raise AssertionError("Unsupported compiler version: {0}".format(solc_version))

    return solc_version


@pytest.fixture()
def is_new_key_format():
    return get_solc_version() in Spec('>=0.4.9')


def pytest_runtest_setup(item):
    if (item.get_marker('requires_standard_json') is not None and
        not solc_supports_standard_json_interface()):
        pytest.skip('requires `--standard-json` support')
