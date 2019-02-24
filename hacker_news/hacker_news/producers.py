import csv
from google.cloud import bigquery

from hacker_news.app_config import app
from hacker_news.pipelines import cleanup_and_save_localy, calculate_stats


# for simple iterator reading
QUERY_LIMIT = 10000

# for parallel producer
AMOUNT_OF_BATCHES = 10
BATCH_SIZE = 10


@app.producer(cleanup_and_save_localy)
def read_google_big_table():
    """
    Simple producer which iterates over google cloud response and yield
    each row as dict.

    Then this data will be added to queue/streaming service, which then
    will be pass to `cleanup_and_save_localy`

    You can have multiple "next" pipelines.
    """
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
    """
    Just simple generator which read file, and convert it to dict format for
    `calculate_stats` pipeline
    """
    with open("local_topic_related_data.csv", "r") as f:
        for row in csv.reader(f):
            yield dict(
                score=row[0],
                time=row[1],
                text=row[3],
                words=row[4]
            )


@app.worker_producer(cleanup_and_save_localy)
def read_google_big_table_parallel():
    """
    Worker producer it's a way to read data in parallel way.

    This function yields generators which will read each batch of data.
    See -> http://stairspy.com/#producer for more info.

    You should init batches by calling:
    `python manage.py producer:init_session hacker_news.read_google_big_table_parallel`

    And then to start reading each batch (in parallel way):
    `python manage.py producer:process hacker_news.read_google_big_table_parallel`
    """
    client = bigquery.Client()

    for i in range(AMOUNT_OF_BATCHES):
        yield read_batch(client, i)


# UTILS

def read_batch(client, batch_id):
    """
    Reading each batch of data
    """
    query = """
    SELECT score, time, type, text
    FROM `bigquery-public-data.hacker_news.full` 
    LIMIT %s OFFSET %s;
    """ % (BATCH_SIZE, batch_id * BATCH_SIZE)

    query_job = client.query(query)
    iterator = query_job.result(timeout=30)

    for row in iterator:
        yield dict(
            score=row[0],
            time=row[1],
            text=row[3],
            words=row[4]
        )
