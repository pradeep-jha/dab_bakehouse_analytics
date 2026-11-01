def test_local_spark_session(local_spark):

    data = [
        ("India", 3),
        ("USA", 2)
    ]

    df = local_spark.createDataFrame(
        data,
        ["country", "customer_count"]
    )

    assert df.count() == 2

    result = {
        row["country"]: row["customer_count"]
        for row in df.collect()
    }

    assert result == {
        "India": 3,
        "USA": 2
    }