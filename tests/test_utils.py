import pytest

import functools
import semantic_version

from solc import get_solc_version
from solc.main import solc_supports_standard_json_interface


SUPPORTED_SOLC_VERSIONS = semantic_version.Spec('>=0.4.1,<=0.4.11')


skipif_no_standard_json = pytest.mark.skipif(
    not solc_supports_standard_json_interface(),
    reason="requires `--standard-json` support"
)


def checks_solc_version(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        solc_version = get_solc_version()

        if solc_version not in SUPPORTED_SOLC_VERSIONS:
            raise AssertionError("Unsupported compiler version: {0}".format(solc_version))

        return fn(*args, **kwargs)
    return inner
