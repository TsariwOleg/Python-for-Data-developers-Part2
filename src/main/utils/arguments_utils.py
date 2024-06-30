"""
Module provides the command-line interface setup for an RSS reader application. It includes functionalities
to parse command-line arguments, validate date formats, and set up the application for use either in a standard
or interactive mode based on the provided inputs.
"""
import argparse
from datetime import datetime
from utils.logging_utils import setup_logging

logger = setup_logging(__name__)

def parser_setup():
    """
    Setup the command-line argument parser for an RSS reader application.

    Returns:
        argparse.ArgumentParser: Configured argument parser for the application.
    """
    parser = argparse.ArgumentParser(
        prog="rss_reader",
        description="Pure Python command-line RSS reader.",
    )

    parser.add_argument(
        "source",
        nargs='?',
        default=None,
        help="RSS URL (optional). If not provided, the application may run in interactive mode."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print result as JSON in stdout. Useful for further processing with tools that accept JSON."
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit the number of news topics returned. Useful for large feeds where you want a quick summary."
    )
    parser.add_argument(
        "--date",
        type=valid_date,
        help="Filter news items by publication date. The date should be provided in YYYYMMDD format."
    )

    return parser


def valid_date(passed_date):
    """
    Validate and convert the input string into a datetime.date object.

    Arguments:
        passed_date (str): Input string representing a date in YYYYMMDD format.

    Returns:
        datetime.date: The validated and converted date.

    Raises:
        argparse.ArgumentTypeError: If the date string does not match the required format or is invalid.
    """
    try:
        return datetime.strptime(passed_date, "%Y%m%d").date()
    except ValueError:
        msg = f"Date {passed_date} is not valid. Date format should be YYYYMMDD."
        logger.error(msg)
        raise argparse.ArgumentTypeError(msg)
