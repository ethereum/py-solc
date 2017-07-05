import os

import pytest

import semantic_version

from solc import (
    get_solc_version,
)
from solc.install import (
    INSTALL_FUNCTIONS,
    get_platform,
    install_solc,
    get_executable_path,
    get_extract_path,
)


INSTALLATION_TEST_PARAMS = tuple(
    (platform, version)
    for platform, platform_install_functions in INSTALL_FUNCTIONS.items()
    for version in platform_install_functions.keys()
)


@pytest.mark.skipif(
    'SOLC_RUN_INSTALL_TESTS' not in os.environ,
    reason=(
        "Installation tests will not run unless `SOLC_RUN_INSTALL_TESTS` "
        "environment variable is set"
    ),
)
@pytest.mark.parametrize(
    "platform,version",
    INSTALLATION_TEST_PARAMS,
)
def test_solc_installation_as_function_call(monkeypatch, tmpdir, platform, version):
    if get_platform() != platform:
        pytest.skip("Wront platform for install script")

    base_install_path = str(tmpdir.mkdir("temporary-dir"))
    monkeypatch.setenv('SOLC_BASE_INSTALL_PATH', base_install_path)

    # sanity check that it's not already installed.
    executable_path = get_executable_path(version)
    assert not os.path.exists(executable_path)

    install_solc(identifier=version, platform=platform)

    assert os.path.exists(executable_path)
    monkeypatch.setenv('SOLC_BINARY', executable_path)

    extract_path = get_extract_path(version)
    if os.path.exists(extract_path):
        contains_so_file = any(
            os.path.basename(path).partition(os.path.extsep)[2] == 'so'
            for path
            in os.listdir(extract_path)
        )
        if contains_so_file:
            monkeypatch.setenv('LD_LIBRARY_PATH', extract_path)

    actual_version = get_solc_version()
    expected_version = semantic_version.Spec(version.lstrip('v'))

    assert actual_version in expected_version
