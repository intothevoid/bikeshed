# Unit tests for app.py
import os
import unittest
from unittest.mock import patch
import subprocess

from app import DOWNLOAD_DIR, already_downloaded, is_disk_space_below_threshold


class AlreadyDownloadedTest(unittest.TestCase):
    # Tests that the function returns True when the magnet link exists in downloaded.txt.
    def test_already_downloaded_exists(self):
        # Setup
        magnet_link = "magnet:?xt=urn:btih:1234567890abcdef"
        with open("downloaded.txt", "w") as f:
            f.write(magnet_link)

        # Test
        result = already_downloaded(magnet_link)

        # Assert
        assert result == True

    # Tests that the function returns False when the magnet link does not exist in downloaded.txt.
    def test_already_downloaded_not_exists(self):
        # Setup
        magnet_link = "magnet:?xt=urn:btih:1234567890abcdef"
        with open("downloaded.txt", "w") as f:
            f.write("magnet:?xt=urn:btih:0987654321fedcba")

        # Test
        result = already_downloaded(magnet_link)

        # Assert
        assert result == False

    def tearDown(self) -> None:
        os.remove("downloaded.txt")
        return super().tearDown()


class IsDiskSpaceBelowThresholdTest(unittest.TestCase):
    @patch("subprocess.run")
    def test_is_disk_space_below_threshold(self, mock_run):
        # Arrange
        mock_output = "Filesystem      Size  Used Avail Use% Mounted on\n/dev/sda1       100G   90G   9G  90% /downloads\n"
        mock_run.return_value.stdout.decode.return_value = mock_output

        # Act
        result = is_disk_space_below_threshold()

        # Assert
        mock_run.assert_called_once_with(
            ["df", "-h", f"{DOWNLOAD_DIR}"], capture_output=True
        )
        self.assertTrue(result)

    @patch("subprocess.run")
    def test_is_disk_space_above_threshold(self, mock_run):
        # Arrange
        mock_output = "Filesystem      Size  Used Avail Use% Mounted on\n/dev/sda1       100G   80G   20G  80% /downloads\n"
        mock_run.return_value.stdout.decode.return_value = mock_output

        # Act
        result = is_disk_space_below_threshold()

        # Assert
        mock_run.assert_called_once_with(
            ["df", "-h", f"{DOWNLOAD_DIR}"], capture_output=True
        )
        self.assertFalse(result)
