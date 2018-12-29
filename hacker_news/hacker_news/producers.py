from google.cloud import bigquery

from hacker_news.app_config import app
from hacker_news.pipelines import cleanup_and_save_localy


QUERY_LIMIT = 10 ** 6


@app.producer(cleanup_and_save_localy)
def read_google_big_table():
    client = bigquery.Client()

    query = """
    SELECT score, time, type, text
    FROM `bigquery-public-data.hacker_news.full`
    LIMIT %s;
    """ % QUERY_LIMIT

    query_job = client.query(query)
    iterator = query_job.result(timeout=30)

    return iterator
