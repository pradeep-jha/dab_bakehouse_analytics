
import os
import sys
import pathlib
import json
import csv

import pytest
from pyspark.sql import SparkSession
from databricks.connect import DatabricksSession
from databricks.sdk import WorkspaceClient


# 1. LOCAL SPARK - Unit tests

@pytest.fixture()
def local_spark():

    session = (
        SparkSession.builder
        .master("local[2]")
        .appName("Customer360-Unit-Tests")
        .getOrCreate()
    )

    yield session

    session.stop()


# 2. DATABRICKS SPARK - Integration tests

def _enable_fallback_compute():

    conf = WorkspaceClient().config

    if (
        conf.serverless_compute_id
        or conf.cluster_id
        or os.environ.get("SPARK_REMOTE")
    ):
        return

    print(
        "No compute specified. Falling back to serverless compute.",
        file=sys.stderr
    )

    os.environ["DATABRICKS_SERVERLESS_COMPUTE_ID"] = "auto"


@pytest.fixture()
def databricks_spark() -> SparkSession:

    _enable_fallback_compute()

    if hasattr(DatabricksSession.builder, "validateSession"):
        session = (
            DatabricksSession.builder
            .validateSession()
            .getOrCreate()
        )
    else:
        session = DatabricksSession.builder.getOrCreate()

    return session


# 3. BACKWARD COMPATIBILITY

@pytest.fixture()
def spark(databricks_spark):
    return databricks_spark


# 4. LOAD TEST FIXTURES

@pytest.fixture()
def load_fixture(spark: SparkSession):

    def _loader(filename: str):

        path = (
            pathlib.Path(__file__).parent.parent
            / "fixtures"
            / filename
        )

        suffix = path.suffix.lower()

        if suffix == ".json":
            rows = json.loads(path.read_text())
            return spark.createDataFrame(rows)

        if suffix == ".csv":
            with path.open(newline="") as f:
                rows = list(csv.DictReader(f))

            return spark.createDataFrame(rows)

        raise ValueError(
            f"Unsupported fixture type for: {filename}"
        )

    return _loader
