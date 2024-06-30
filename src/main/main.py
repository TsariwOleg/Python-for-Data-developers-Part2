"""
This module provides a command-line tool to fetch, parse, and cache RSS feeds using Apache Spark.
It is designed to handle RSS feeds by fetching data from provided URLs, parsing it into structured formats,
caching it for efficiency, and allowing the user to filter cached data by date.
"""

import sys
from pyspark.sql import SparkSession

from entity.entity import Channel
from utils.logging_utils import setup_logging
from utils.rss_utils import fetch_rss_feed, rss_parser
from utils.cache_utils import write_cache, read_cache
from utils.arguments_utils import parser_setup

logger = setup_logging(__name__)


def initialize_spark(app_name="default_name"):
    """
    Set the Python executable for PySpark to the current Python executable to ensure compatibility
    with the current environment.

    Arguments:
        app_name (str): The name of the Spark application. Defaults to "default_name".

    Returns:
        SparkSession: An initialized SparkSession.
    """
    try:
        spark = SparkSession \
            .builder \
            .appName(app_name) \
            .config("spark.sql.sources.partitionOverwriteMode", "dynamic") \
            .getOrCreate()

        spark.sparkContext.setLogLevel("OFF")

        return spark
    except Exception as e:
        logger.error(f"Failed to initialize Spark session: {e}")
        raise


def process_with_cache_or_fetch(spark, source, date):
    """
    Process RSS feed data.

    Arguments:
        spark (SparkSession): The Spark session object.
        source (str): URL of the RSS feed.
        date (datetime): Specific date to filter the RSS feed items.

    Returns:
        list: A list of processed Channel objects.

    Raises:
        Exception: If no cached or fetched data is available.
    """
    if date:
        cache = read_cache(spark, source)
        returned_list = list(map(lambda x: x.filter_items(date), cache))
        not_empty_list = list(filter(lambda x: x.item, cache))

        if len(not_empty_list) == 0:
            raise Exception("No data found for the specified date.")
        return returned_list
    else:
        fetched_rss = fetch_rss_feed(source)
        parsed_rdd = rss_parser(source, fetched_rss)
        write_cache(parsed_rdd, spark)
        return [parsed_rdd]


def main(passed_args):
    """
    Main function to execute the RSS feed processing.

    Arguments:
        passed_args: Command-line arguments.

    Returns:
        str: Processed results formatted as specified (JSON or plain text).
    """
    spark = initialize_spark("test")
    res = process_with_cache_or_fetch(spark, passed_args.source, passed_args.date)
    final_res = list(map(lambda x: Channel.create_output(x, passed_args.json, passed_args.limit), res))
    return "\n\n".join(final_res)


if __name__ == "__main__":
    """
    The main block parses command-line arguments and calls the main function.
    """
    parser = parser_setup()
    args = parser.parse_args(sys.argv[1:])

    if not args.date and not args.source:
        parser.error("The following arguments are required: --date or source")

    print(main(args))
