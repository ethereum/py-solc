import pytest
import semantic_version


@pytest.fixture()
def contracts_dir(tmpdir):
    return str(tmpdir.mkdir("contracts"))


@pytest.fixture(scope="session")
def SUPPORTED_SOLC_VERSIONS():
    return semantic_version.Spec('>=0.4.1,<=0.4.11')
