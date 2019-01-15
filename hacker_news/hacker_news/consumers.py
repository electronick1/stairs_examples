import redis
import csv
from hacker_news.app_config import app


redis_db = redis.Redis(host=app.config.agregation_redis_host,
                       port=app.config.agregation_redis_port)

local_topic_writer = csv.writer(open("local_topic_related_data.csv", "a"))


@app.standalone_consumer()
def save_topic_related_data(score, time, type, text, words, stemmed_words):
    global local_topic_writer
    local_topic_writer.writerow((score, time, type, text, words, stemmed_words))


@app.consumer()
def aggregate_average_value(value, agregation_name):
    if isinstance(value, list):
        for v in value:
            redis_db.hincrby(agregation_name, v, 1)
    else:
        redis_db.lpush(agregation_name, value)
