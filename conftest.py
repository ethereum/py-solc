import pytest
import semantic_version


@pytest.fixture()
def contracts_dir(tmpdir):
    return str(tmpdir.mkdir("contracts"))
