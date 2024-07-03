import os
from transfer_media.main import transfer
from unittest.mock import patch


@patch(
    "builtins.input",
    side_effect=[
        "1",
        "2",
    ],
)
def test_detect_existing_different_file(magic_mock, caplog):
    transfer(
        volume_directory=os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "test_detect_existing_different_file"
            )
        )
    )
    assert (
        'Detected duplicate file "Videos/2024/07-Jul" with the same name, not overriding'
        in caplog.text
    )
