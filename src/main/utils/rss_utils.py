"""
This module provides functions for fetching and parsing RSS feeds. It uses the `requests` library to retrieve
RSS feed data from a given source URL and then parses the XML content into structured data.
"""

import requests
import xmltodict
from entity.entity import Channel
from utils.logging_utils import setup_logging

logger = setup_logging(__name__)


def fetch_rss_feed(source: str):
    """
    Fetch the RSS feed data from a given source URL.

    Arguments:
        source (str): The URL of the RSS feed.

    Returns:
        str: The XML content of the RSS feed.

    Raises:
        requests.exceptions.HTTPError: If an HTTP error occurs.
        requests.exceptions.ConnectionError: If a connection error occurs.
        requests.exceptions.Timeout: If the request times out.
        requests.exceptions.RequestException: For other request-related errors.
    """
    try:
        response = requests.get(source)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        raise
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Connection error occurred: {conn_err}")
        raise
    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Timeout error occurred: {timeout_err}")
        raise
    except requests.exceptions.RequestException as req_err:
        logger.error(f"An error occurred: {req_err}")
        raise


def rss_parser(source: str, xml: str):
    """
    Parse the XML content of an RSS feed into a Channel object.

    Arguments:
        source (str): The source URL of the RSS feed, used as a reference in the Channel object.
        xml (str): The XML content of the RSS feed.

    Returns:
        Channel: A Channel object populated with data from the RSS feed.

    Raises:
        ValueError: If the XML data does not contain the required 'channel' element.
        Exception: For unexpected errors during the parsing process.
    """
    try:
        dict_data = xmltodict.parse(xml)
        root = dict_data.get("rss").get("channel")
        if root is None:
            msg = "Invalid RSS feed format: missing 'channel' element"
            logger.error(msg)
            raise ValueError(msg)
        return Channel(source, **root)
    except ValueError as val_err:
        logger.error(f"Value error: {val_err}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise
