# Unit tests for motogp_dl.py
import os
import unittest
from unittest.mock import patch

import requests
from gotify.message import send_gotify_message
from motogp_dl import DOWNLOAD_DIR, already_downloaded, is_disk_space_below_threshold
from util.log import LOGGER


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
    @patch("motogp_dl.psutil.disk_usage")
    def test_below_threshold(self, mock_disk_usage):
        mock_disk_usage.return_value.free = 5 * (2**30)  # set free space to 5GB
        self.assertTrue(
            is_disk_space_below_threshold(10)
        )  # check if space is below threshold of 10GB

    @patch("motogp_dl.psutil.disk_usage")
    def test_above_threshold(self, mock_disk_usage):
        mock_disk_usage.return_value.free = 15 * (2**30)  # set free space to 15GB
        self.assertFalse(
            is_disk_space_below_threshold(10)
        )  # check if space is above threshold of 10GB


class GotifyTest(unittest.TestCase):
    # Tests that a message is successfully sent to gotify when all inputs are valid.
    @patch("gotify.message.requests.post")
    def test_send_gotify_message_with_valid_inputs(self, mocker):
        # arrange
        os.environ["GOTIFY_TOKEN"] = "token"
        os.environ["GOTIFY_URL"] = "url"
        os.environ["GOTIFY_APP_ID"] = "app_id"

        # act
        send_gotify_message("test message")

        # assert
        requests.post.assert_called_once_with(
            f"url/message?token=token&app=app_id",
            json={
                "message": "test message",
                "priority": 5,
                "title": "motogp_dl",
                "extras": None,
            },
        )
