from main import initialize_spark
import pytest  # install
from unittest import mock
from pyspark.sql import SparkSession


def test_initialize_spark_exception():
    with mock.patch.object(SparkSession.builder, 'getOrCreate', side_effect=Exception("Test exception")):
        with pytest.raises(Exception, match="Test exception"):
            initialize_spark("test_app")
