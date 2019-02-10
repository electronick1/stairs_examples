import redis
import csv
from hacker_news.app_config import app


# Here we connection to the redis which will aggregate all stats values
# Note: we are using app.config here, which allows us to change host/port
# if this app will be used in another project
redis_db = redis.Redis(host=app.config.agregation_redis_host,
                       port=app.config.agregation_redis_port)

local_topic_writer = csv.writer(open("local_topic_related_data.csv", "a"))


@app.standalone_consumer()
def save_topic_related_data(score, time, type, text, words, stemmed_words):
    """
    This standalone consumer allows you to run separate process to read data
    from queue/streaming service. It's useful when you want to collect data
    in "one place" or write it file.

    Run:
    `python manager.py consumer:standalone hacker_news.save_topic_related_data`

    To start reading queue/streaming service.
    """
    global local_topic_writer
    local_topic_writer.writerow((score, time, type, text, words, stemmed_words))


@app.consumer()
def aggregate_average_value(value, agregation_name):
    """
    It's a simple consumer which run inside pipeline environment. You can
    also make it as a worker just defining "as_worker=True" inside pipeline.

    In most cases it not improve your performance, but make saving process
    more "save" if some e.g. connection fails.
    """
    if isinstance(value, list):
        for v in value:
            # inc redis key
            redis_db.hincrby(agregation_name, v, 1)
    else:
        # Just add name to this list
        redis_db.lpush(agregation_name, value)
