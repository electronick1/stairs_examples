import csv
from google.cloud import bigquery

from hacker_news.app_config import app
from hacker_news.pipelines import cleanup_and_save_localy, calculate_stats


QUERY_LIMIT = 10000


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

    for row in iterator:
        yield dict(
            score=row[0],
            time=row[1],
            type=row[2],
            text=row[3],
        )


@app.producer(calculate_stats)
def read_top_file():
    with open("local_topic_related_data.csv", "r") as f:
        for row in csv.reader(f):
            yield dict(
                score=row[0],
                time=row[1],
                text=row[3],
                words=row[4]
            )
