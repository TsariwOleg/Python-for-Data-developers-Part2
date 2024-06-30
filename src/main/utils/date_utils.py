"""
Module handles the parsing of date strings with time zone information using the `dateutil` library.
"""
import pytz
from dateutil import parser


def parse_date_with_timezone(date_string):
    """
    Parses a date string that includes a timezone abbreviation into a timezone-aware datetime object.

    Arguments:
        date_string (str): The date string to be parsed, which should include a timezone abbreviation.

    Returns:
        datetime.datetime: A timezone-aware datetime object corresponding to the given date string.
    """
    tz_info = {
        'CST': pytz.timezone('America/Chicago'),
        'CDT': pytz.timezone('America/Chicago'),
        'EDT': pytz.timezone('America/New_York')
    }
    return parser.parse(date_string, tzinfos=tz_info)
