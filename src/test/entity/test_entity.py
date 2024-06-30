import pytest
from datetime import datetime
import json as js

from entity.entity import Channel, Item  # Adjust import paths according to your project structure
from utils.date_utils import parse_date_with_timezone

# Sample data for testing
sample_channel_data = {
    "source": "http://www.example.com/rss",
    "title": "Test RSS Feed",
    "link": "http://www.example.com/",
    "lastBuildDate": "Fri, 21 Jul 2023 09:04 EDT",
    "pubDate": "Fri, 21 Jul 2023 09:04 EDT",
    "language": "en",
    "category": ['Media', {'@domain': 'Newspapers/Regional/United_States', '#text': "News"}],
    "managingEditor": "editor@example.com",
    "description": "This is a test RSS feed",
    "item": [
        {
            "title": "Test Item 1",
            "author": "Author 1",
            "pubDate": "Fri, 21 Jul 2023 09:04 EDT",
            "link": "http://www.example.com/test-item-1",
            "category": "Category 1",
            "description": "This is a test item 1"
        },
        {
            "title": "Test Item 2",
            "author": "Author 2",
            "pubDate": "Sat, 22 Jul 2023 09:04 EDT",
            "link": "http://www.example.com/test-item-2",
            "category": "Category 2",
            "description": "This is a test item 2"
        }
    ]
}


def test_channel_initialization():
    channel = Channel(**sample_channel_data)
    assert channel.source == sample_channel_data["source"]
    assert channel.title == sample_channel_data["title"]
    assert channel.link == sample_channel_data["link"]
    assert channel.lastBuildDate == sample_channel_data["lastBuildDate"]
    assert channel.pubDate == sample_channel_data["pubDate"]
    assert channel.language == sample_channel_data["language"]
    assert channel.category == "Media, News"
    assert channel.managingEditor == sample_channel_data["managingEditor"]
    assert channel.description == sample_channel_data["description"]
    assert len(channel.item) == 2
    assert channel.item[0].title == sample_channel_data["item"][0]["title"]
    assert channel.item[1].title == sample_channel_data["item"][1]["title"]


def test_item_initialization():
    item_data = sample_channel_data["item"][0]
    item = Item(**item_data)
    assert item.title == item_data["title"]
    assert item.author == item_data["author"]
    assert item.pubDate == item_data["pubDate"]
    assert item.link == item_data["link"]
    assert item.category == item_data["category"]
    assert item.description == item_data["description"]


def test_channel_filter_items():
    channel = Channel(**sample_channel_data)
    filter_date = datetime(2023, 7, 21).date()
    channel.filter_items(filter_date)
    assert len(channel.item) == 1

    filter_date = datetime(2023, 7, 22).date()
    channel.filter_items(filter_date)
    assert len(channel.item) == 0


def test_channel_to_dict():
    channel = Channel(**sample_channel_data)
    channel_dict = channel.to_dict()
    assert channel_dict["source"] == sample_channel_data["source"]
    assert channel_dict["title"] == sample_channel_data["title"]
    assert channel_dict["link"] == sample_channel_data["link"]
    assert channel_dict["lastBuildDate"] == sample_channel_data["lastBuildDate"]
    assert channel_dict["pubDate"] == sample_channel_data["pubDate"]
    assert channel_dict["language"] == sample_channel_data["language"]
    assert channel_dict["category"] == "Media, News"
    assert channel_dict["managingEditor"] == sample_channel_data["managingEditor"]
    assert channel_dict["description"] == sample_channel_data["description"]
    assert len(channel_dict["item"]) == 2


def test_item_to_dict():
    item_data = sample_channel_data["item"][0]
    item = Item(**item_data)
    item_dict = item.to_dict()
    assert item_dict["title"] == item_data["title"]
    assert item_dict["author"] == item_data["author"]
    assert item_dict["pubDate"] == item_data["pubDate"]
    assert item_dict["link"] == item_data["link"]
    assert item_dict["category"] == item_data["category"]
    assert item_dict["description"] == item_data["description"]


def test_channel_create_output():
    channel = Channel(**sample_channel_data)
    output = Channel.create_output(channel, json=True, limit=1)
    output_dict = js.loads(output)
    assert output_dict["title"] == sample_channel_data["title"]
    assert output_dict["link"] == sample_channel_data["link"]
    assert len(output_dict["item"]) == 1
    assert output_dict["item"][0]["title"] == sample_channel_data["item"][0]["title"]


def test_item_create_common_output():
    item_data = sample_channel_data["item"][0]
    item = Item(**item_data)
    common_output = Item.create_common_output(item.to_dict())
    assert "Title: Test Item 1" in common_output
    assert "Author: Author 1" in common_output
