from stairs import concatenate

from hacker_news.app_config import app
from hacker_news.flows.cleanup import PrepareText, FilterComments
from hacker_news.flows.stats import (CalculateSentiment,
                                     CalculateMentionedLibs)

from hacker_news.consumers import save_topic_related_data, aggregate_value


@app.pipeline(config=dict(filter_comments=dict(topic='python')))
def cleanup_and_save_localy(pipeline, score, time, type, text):
    hacker_news_record = concatenate(
        score=score,
        time=time,
        type=type,
        text=text
    )

    filter_comments_flow = FilterComments(**pipeline.config['filter_comments'])

    return hacker_news_record.subscribe_flow(PrepareText())\
                             .subscribe_flow(filter_comments_flow)\
                             .subscribe_consumer(save_topic_related_data)


@app.pipeline()
def calculate_stats(pipeline, score, time, text, words):
    data = concatenate(score=score, time=time, words=words)

    sentiment = text\
        .apply_flow(CalculateSentiment(), as_worker=True) \
        .make(value="sentiment") \
        .subscribe_consumer(aggregate_value)

    libs = data\
        .apply_flow(CalculateMentionedLibs()) \
        .make(value="libs") \
        .subscribe_consumer(aggregate_value)

    return concatenate(sentiment=sentiment, libs=libs)
