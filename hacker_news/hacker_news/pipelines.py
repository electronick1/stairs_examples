from stairs import concatenate

from hacker_news.app_config import app
from hacker_news.flows.cleanup import PrepareText, FilterComments
from hacker_news.flows.stats import (CalculateSentiment,
                                     CalculateMentionedLibs)

from hacker_news.consumers import (save_topic_related_data,
                                   aggregate_average_value)


@app.pipeline(config=dict(filter_comments=dict(topic='python')))
def cleanup_and_save_localy(pipeline, score, time, type, text):
    """
    It's a function which build's data pipeline.

    First arg is always pipeline object, which used to extract config or
    any other meta information about pipeline.

    Next we have args which defines a data. All of them are stairs.DataPoint
    it's not represent "real" data from producer, it's just a "mock" of your
    data.

    Here we are using "config" argument inside pipeline, just to define
    "default" arguments for `Filter` flow, you can easily change this config
    vars from another pipeline.

    :param pipeline: stairs.WorkerInfo
    :param score: stairs.DataPoint
    :param time: stairs.DataPoint
    :param type: stairs.DataPoint
    :param text: stairs.DataPoint
    :return: stairs.DataFrame
    """

    # Concatenate all DataPoint's to one object called `DataFrame`
    hacker_news_record = concatenate(
        score=score,
        time=time,
        type=type,
        text=text
    )

    # Here we initialize Filter flow based on pipeline config
    filter_comments_flow = FilterComments(**pipeline.config['filter_comments'])

    # Here we are building pipeline, simple subscribing Flows (of functions)
    # to data.
    # And then save everything localy using "save_topic_related_data" consumer
    return hacker_news_record.subscribe_flow(PrepareText())\
                             .subscribe_flow(filter_comments_flow)\
                             .subscribe_consumer(save_topic_related_data)


@app.pipeline()
def calculate_stats(pipeline, score, time, text, words):
    """
    Here we have pipeline which calculated sentiment and mentions stats
    based on filtered local data from `cleanup_and_save_localy`

    Data to this pipeline comes from `read_top_file` producer.

    We creating two "branches" of data processing and then concatenate them
    to one data frame, you can make any of pipeline components as "worker"
    simple set "as_worker=True"

    :param pipeline: stairs.WorkerInfo
    :param score: stairs.DataPoint
    :param time: stairs.DataPoint
    :param text: stairs.DataPoint
    :param words: stairs.DataPoint
    :return: stairs.DataFrame
    """

    # Concatenate all DataPoint's to one object called `DataFrame`
    data = concatenate(score=score, time=time, words=words)

    # Calculate Sentiment first
    # Here CalculateSentiment called as a worker, it means all data will be
    # send to CalculateSentiment using queue/streaming service and
    # process in a fast/safe way.
    sentiment = text\
        .apply_flow(CalculateSentiment(), as_worker=True) \
        .rename(value="sentiment") \
        .add_value(agregation_name="sentiment")\
        .subscribe_consumer(aggregate_average_value)

    libs = data\
        .apply_flow(CalculateMentionedLibs()) \
        .rename(value="libs") \
        .add_value(agregation_name="libs") \
        .subscribe_consumer(aggregate_average_value)

    # Concatenate everything to one Data Frame. For now, each pipeline should
    # return only one DataFrame/DataPoint
    return concatenate(sentiment=sentiment, libs=libs)
