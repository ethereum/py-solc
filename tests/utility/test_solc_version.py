import re

from solc import get_solc_version


def test_get_solc_version():
    raw_version_string = get_solc_version()
    version, _, commit_sha = raw_version_string.partition('-')
    assert version
    assert commit_sha

    major, minor, patch = version.split('.')

    assert major.isdigit()
    assert minor.isdigit()
    assert patch.isdigit()
