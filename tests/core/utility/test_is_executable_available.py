from solc.utils.filesystem import (
    is_executable_available,
)


def test_ls_is_available():
    assert is_executable_available('ls') is True


def test_for_unavailable_executable():
    assert is_executable_available('there_should_not_be_an_executable_by_this_name') is False
