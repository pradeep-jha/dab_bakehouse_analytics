#/*********For testing the unit test in ci/cd *********/


def build_customer_360(spark, source_table):

    query = f"""
        SELECT
            country,
            COUNT(*) AS number_of_customer,
            COUNT_IF(gender = 'female') AS female_customers,
            COUNT_IF(gender = 'male') AS male_customers
        FROM {source_table}
        GROUP BY country
    """

    return spark.sql(query)