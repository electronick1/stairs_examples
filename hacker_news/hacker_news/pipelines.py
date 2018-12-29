from stairs import concatinate

from hacker_news.app_config import app
from hacker_news.flows.cleanup import PrepareText, FilterComments
from hacker_news.consumers import save_topic_related_data


@app.pipeline()
def cleanup_and_save_localy(pipeline, score, time, type, text):

    hacker_news_record = concatinate(
        score=score,
        time=time,
        type=type,
        text=text
    )

    filter_comments_flow = FilterComments(pipeline.config.FilterComments)

    return hacker_news_record.subscribe_flow(PrepareText())\
                             .subscribe_flow(filter_comments_flow)\
                             .subscribe_consumer(save_topic_related_data,
                                                 as_worker=True)


@app.pipeline(based_on=cleanup_and_save_localy)
def clean2(pipeline, score, time, type, text):
    pipeline.replace("asd", FilterComments2())
    p1 = pipeline.until("asd")
    p2 = pipeline.after("dsa")
    return p1 + p2