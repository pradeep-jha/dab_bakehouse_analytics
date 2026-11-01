from pyspark.sql import SparkSession
from customer_360_base import build_customer_360


def test_build_customer_360(spark):

    # Step 1: Create sample test data ..
    data = [
        ("India", "female"),
        ("India", "female"),
        ("India", "male"),
        ("USA", "female"),
        ("USA", "male")
    ]

    columns = ["country", "gender"]

    test_df = spark.createDataFrame(data, columns)

    # Step 2: Create temporary source table
    test_df.createOrReplaceTempView("test_customers")

    # Step 3: Execute transformation
    result = build_customer_360(
        spark,
        "test_customers"
    )

    # Step 4: Collect actual output
    actual = {
        row["country"]: (
            row["number_of_customer"],
            row["female_customers"],
            row["male_customers"]
        )
        for row in result.collect()
    }

    # Step 5: Define expected output
    expected = {
        "India": (3, 2, 1),
        "USA": (2, 1, 1)
    }

    # Step 6: Validate output
    assert actual == expected