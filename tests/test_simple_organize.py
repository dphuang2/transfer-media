import os
import pytest
from transfer_media.main import transfer
from unittest.mock import patch
import datetime


@pytest.fixture
def volume_directory():
    # Setup
    directory_to_organize = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "test_simple_organize")
    )
    output_path = os.path.join(directory_to_organize)
    os.makedirs(output_path, exist_ok=True)

    # Create tmp directory with a bunch of .mp4 files
    tmp_path = os.path.join(directory_to_organize, "tmp")
    os.makedirs(tmp_path, exist_ok=True)
    for i in range(5):
        file_path = os.path.join(tmp_path, f"test_{i}.mp4")
        with open(file_path, "wb") as f:
            f.write(os.urandom(1024))  # Create a dummy .mp4 file with random content
        # Modify the created dates on all the files to some random values
        random_date = datetime.datetime(2020 + i, 1, 1).timestamp()
        os.utime(file_path, (random_date, random_date))

    # Teardown
    yield directory_to_organize


@patch(
    "builtins.input",
    side_effect=[
        "1",
        "2",
    ],
)
@pytest.mark.skip(reason="Skipping this test")
def test_simple_organize(mock_input, volume_directory):
    transfer(volume_directory=volume_directory)

    output_path = os.path.join(volume_directory, "output")
    output_mp4_files = []
    for root, dirs, files in os.walk(output_path):
        for file in files:
            if file.lower().endswith(".mp4"):
                output_mp4_files.append(os.path.join(root, file))

    assert any(
        "test.mp4" in file for file in output_mp4_files
    ), "test.mp4 not found in output_path"
