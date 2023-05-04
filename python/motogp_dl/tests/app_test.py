# Unit tests for app.py
import unittest

from app import already_downloaded


class TestApp(unittest.TestCase):
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
