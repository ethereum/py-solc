import re

from solc import get_solc_version


def test_get_solc_version():
    version = get_solc_version()

    assert version

    major, minor, patch = version.split('.')

    assert major.isdigit()
    assert minor.isdigit()
    assert patch.isdigit()
