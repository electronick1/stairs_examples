from hacker_news.app_config import app


@app.consumer()
def save_topic_related_data(score, time, type, text, words, stemmed_words):
    pass