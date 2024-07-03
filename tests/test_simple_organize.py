import os
import pytest
from transfer_media.main import organize
from unittest.mock import patch
import datetime


@pytest.fixture
def volume_directory():
    test_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "test_simple_organize")
    )
    directory_to_organize = os.path.abspath(os.path.join(test_dir, "Videos"))
    os.makedirs(directory_to_organize, exist_ok=True)
    for i in range(5):
        file_path = os.path.join(directory_to_organize, f"test_{i}.mp4")
        with open(file_path, "wb") as f:
            f.write(os.urandom(1024))  # Create a dummy .mp4 file with random content
        # Modify the created dates on all the files to some random values
        random_date = datetime.datetime(2020 + i, 1, 1).timestamp()
        os.utime(file_path, (random_date, random_date))

    yield directory_to_organize

    # delete every file except for .gitkeep in test_simple_organize
    for root, dirs, files in os.walk(test_dir):
        for file in files:
            if file != ".gitkeep":
                os.remove(os.path.join(root, file))

    # delete Videos_Original
    directory_to_organize_original = os.path.abspath(
        os.path.join(test_dir, "Videos_Original")
    )
    if os.path.exists(directory_to_organize_original):
        os.rmdir(directory_to_organize_original)


def test_simple_organize(volume_directory):
    organize(directory=volume_directory)
