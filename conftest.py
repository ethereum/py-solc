import pytest


@pytest.fixture()
def contracts_dir(tmpdir):
    return str(tmpdir.mkdir("contracts"))


@pytest.fixture(scope="session")
def SUPPORTED_SOLC_VERSIONS():
    return {
        "0.4.1",
        "0.4.2",
        "0.4.4",
        "0.4.6",
        "0.4.7",
        "0.4.8",
        "0.4.9",
    }
