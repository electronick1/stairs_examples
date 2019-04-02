
from .app_config import app

from .flows import ExtractCompetitions, ExtractDiscussions, SearchForGHRepos, \
                MentionsKaggle
from .consumers import save_gh_repo, aggregate_monthly


@app.pipeline()
def parse_gh_repos(pipeline, competitions_url):
    """
    Pipeline which trying to extract github urls from kaggle discussions.

    Each flow in this pipeline return a list of data as a result and plays
    "producer" role.
    """
    return competitions_url\
        .subscribe_flow_as_producer(ExtractCompetitions(cnt_pages=50), as_worker=True)\
        .subscribe_flow_as_producer(ExtractDiscussions(), as_worker=True)\
        .subscribe_flow_as_producer(SearchForGHRepos(), as_worker=True)\
        .subscribe_consumer(save_gh_repo)


@app.pipeline()
def parse_mentions(pipeline, competitions_url):
    """
    Pipeline which trying to extract github urls from kaggle discussions.

    Each flow in this pipeline return a list of data as a result and plays
    "producer" role.
    """
    return competitions_url\
        .subscribe_flow_as_producer(ExtractCompetitions(cnt_pages=50), as_worker=True)\
        .subscribe_flow_as_producer(ExtractDiscussions(), as_worker=True)\
        .subscribe_flow(MentionsKaggle(terms=['boosting']), as_worker=True)\
        .add_value(key="mentions_in_competitions")\
        .rename(has_action='cnt_mentions')\
        .subscribe_consumer(aggregate_monthly)
