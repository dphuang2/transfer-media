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
    import io
    import sys

    captured_output = io.StringIO()
    sys.stdout = captured_output

    main(
        volume_directory=os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "test_detect_existing_different_file"
            )
        )
    )

    sys.stdout = sys.__stdout__
    output_string = captured_output.getvalue()
    assert (
        'Detected duplicate file "Videos/2024/07-Jul" with the same name, not overriding'
        in output_string
    )
