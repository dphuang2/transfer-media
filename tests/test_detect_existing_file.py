import os
from transfer_media.main import main
from unittest.mock import patch


@patch(
    "builtins.input",
    side_effect=[
        "1",
        "2",
    ],
)
def test_detect_existing_file(self):
    main(
        test_dir=os.path.abspath(
            os.path.join(os.path.dirname(__file__), "test_detect_existing_file")
        )
    )
