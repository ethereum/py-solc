import pytest


@pytest.fixture()
def contracts_dir(tmpdir):
    return str(tmpdir.mkdir("contracts"))
