import os
import pytest
from transfer_media.main import main
from unittest.mock import patch


@pytest.fixture
def volume_directory():
    # Setup
    volume_directory = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "test_simple_copy")
    )
    output_path = os.path.join(volume_directory, "output")
    os.makedirs(output_path, exist_ok=True)

    # Teardown
    yield volume_directory

    # Cleanup
    for root, dirs, files in os.walk(output_path):
        for file in files:
            if file.lower().endswith(".mp4"):
                os.remove(os.path.join(root, file))


@patch(
    "builtins.input",
    side_effect=[
        "1",
        "2",
    ],
)
def test_simple_copy(mock_input, volume_directory):
    main(volume_directory=volume_directory)

    output_path = os.path.join(volume_directory, "output")
    output_mp4_files = []
    for root, dirs, files in os.walk(output_path):
        for file in files:
            if file.lower().endswith(".mp4"):
                output_mp4_files.append(os.path.join(root, file))

    assert any(
        "test.mp4" in file for file in output_mp4_files
    ), "test.mp4 not found in output_path"
