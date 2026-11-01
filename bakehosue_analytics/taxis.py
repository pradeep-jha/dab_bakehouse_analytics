from pyspark.sql import DataFrame, SparkSession


def find_all_taxis(spark: SparkSession) -> DataFrame:
    """Find all taxi data."""
    return spark.read.table("samples.nyctaxi.trips")