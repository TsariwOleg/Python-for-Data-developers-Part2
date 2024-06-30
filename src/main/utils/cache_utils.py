"""
Module provides functionality for caching and retrieving Channel data using PySpark. It includes functions to
write Channel objects to a cache in Parquet format and read them back into the application. The caching mechanism is
designed to support efficient data retrieval based on the source attribute, enabling quick access to channel data for
RSS feeds.
"""
from pyspark.sql import SparkSession
from entity.entity import Channel
from pyspark.sql.functions import col


def write_cache(channel: Channel, spark: SparkSession):
    """
    Writes the channel information, partitioned by the source URL.

    Arguments:
        channel (Channel): The Channel object to be cached.
        spark (SparkSession): The SparkSession object to use for DataFrame operations.
    """
    df = spark.sparkContext.parallelize([channel.to_dict()]).toDF()
    df.write.format("parquet").partitionBy('source').mode("overwrite").save(".cache/")


def read_cache(spark: SparkSession, source: str) -> list:
    """
    Reads the channel information from cache.

    Arguments:
        spark (SparkSession): The SparkSession object to use for reading data.
        source (str): The source URL. If not provided, all cached data is returned.

    Returns:
        list: A list of Channel objects retrieved from the cache.
    """
    cache_df = spark.read.format("parquet").load(".cache/")

    if source:
        cache_df = cache_df.where(col("source") == source)

    return list(map(lambda x: Channel.from_dict(x.asDict()), cache_df.collect()))
