# from bakehosue_analytics import taxis
from bakehosue_analytics import taxis

def test_find_all_taxis(spark):
    results = taxis.find_all_taxis(spark)

    assert results is not None