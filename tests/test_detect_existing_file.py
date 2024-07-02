import os
from transfer_media.main import main
from unittest.mock import patch
import logging


@patch(
    "builtins.input",
    side_effect=[
        "1",
        "2",
    ],
)
def test_detect_existing_file(magic_mock, caplog):
    main(
        volume_directory=os.path.abspath(
            os.path.join(os.path.dirname(__file__), "test_detect_existing_file")
        )
    )
    assert 'Detected duplicate file "Videos/2024/06-Jun", not overriding' in caplog.text
