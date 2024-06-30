import pytest
from unittest import mock
import requests
import xmltodict

from utils.rss_utils import fetch_rss_feed, rss_parser  # Adjust this import according to your project structure
from entity.entity import Channel  # Ensure this import path is correct

# Mock RSS feed data for testing
valid_rss_feed = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>Test RSS Feed</title>
    <link>http://www.example.com/</link>
    <description>This is a test RSS feed</description>
    <item>
      <title>Test Item</title>
      <link>http://www.example.com/test-item</link>
      <description>This is a test item</description>
      <pubDate>Fri, 21 Jul 2023 09:04 EDT</pubDate>
    </item>
  </channel>
</rss>
"""

invalid_rss_feed = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
</rss>
"""


def test_fetch_rss_feed_success():
    with mock.patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = valid_rss_feed

        result = fetch_rss_feed("http://www.example.com/rss")

        assert result == valid_rss_feed


def test_fetch_rss_feed_error():
    with mock.patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.HTTPError("HTTP error")
        with pytest.raises(requests.exceptions.HTTPError):
            fetch_rss_feed("http://www.example.com/rss")

    with mock.patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")
        with pytest.raises(requests.exceptions.ConnectionError):
            fetch_rss_feed("http://www.example.com/rss")

    with mock.patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout("Timeout error")
        with pytest.raises(requests.exceptions.Timeout):
            fetch_rss_feed("http://www.example.com/rss")

    with mock.patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("Request error")
        with pytest.raises(requests.exceptions.RequestException):
            fetch_rss_feed("http://www.example.com/rss")


def test_rss_parser_valid_feed():
    result = rss_parser("http://www.example.com/rss", valid_rss_feed)

    assert isinstance(result, Channel)
    assert result.title == "Test RSS Feed"
    assert result.link == "http://www.example.com/"
    assert len(result.item) == 1
    assert result.item[0].title == "Test Item"


def test_rss_parser_invalid_feed():
    with pytest.raises(ValueError, match="Invalid RSS feed format: missing 'channel' element"):
        rss_parser("http://www.example.com/rss", invalid_rss_feed)
