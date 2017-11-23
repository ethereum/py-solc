from solc import get_solc_version

import semantic_version


def test_get_solc_version():
    version = get_solc_version()

    assert isinstance(version, semantic_version.Version)
