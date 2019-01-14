import csv
from hacker_news.app_config import app


local_topic_writer = csv.writer(open("local_topic_related_data.csv", "a"))


@app.standalone_consumer()
def save_topic_related_data(score, time, type, text, words, stemmed_words):
    global local_topic_writer
    local_topic_writer.writerow((score, time, type, text, words, stemmed_words))


@app.consumer()
def aggregate_value(value):
    pass
