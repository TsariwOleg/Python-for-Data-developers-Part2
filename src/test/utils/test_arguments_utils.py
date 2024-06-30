import pytest
from datetime import datetime
from argparse import ArgumentParser, ArgumentTypeError
from utils.arguments_utils import parser_setup, valid_date


def test_valid_date():
    assert valid_date("20230621") == datetime(2023, 6, 21).date()
    with pytest.raises(ArgumentTypeError):
        valid_date("2023-06-21")
    with pytest.raises(ArgumentTypeError):
        valid_date("invalid-date")


def test_parser_setup():
    parser = parser_setup()

    args = parser.parse_args([])
    assert args.source is None
    assert args.json is False
    assert args.limit is None
    assert args.date is None

    args = parser.parse_args(["http://example.com/rss", "--json", "--limit", "10", "--date", "20230621"])
    assert args.source == "http://example.com/rss"
    assert args.json is True
    assert args.limit == 10
    assert args.date == datetime(2023, 6, 21).date()
