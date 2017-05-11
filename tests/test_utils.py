import pytest
from solc.main import solc_supports_standard_json_interface

skipif_no_standard_json = pytest.mark.skipif(
    not solc_supports_standard_json_interface(),
    reason="requires `--standard-json` support"
)
