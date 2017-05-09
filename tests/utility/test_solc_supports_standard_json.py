from solc import get_solc_version
from solc.main import solc_supports_standard_json_interface

import semantic_version


def test_get_solc_version():
    version = get_solc_version()

    if version in semantic_version.Spec("<0.4.11"):
    	assert not solc_supports_standard_json_interface()
    else:
    	assert solc_supports_standard_json_interface()
