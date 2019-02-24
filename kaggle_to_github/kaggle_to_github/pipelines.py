
from .app_config import app

from .flows import ExtractCompetitions, ExtractDiscussions, SearchForGHRepos
from .consumers import save_gh_repo


@app.pipeline()
def parse_gh_repos(pipeline, competitions_url):
    """
    Pipeline which trying to extract github urls from kaggle discussions.

    Each flow in this pipeline return a list of data as a result and plays
    "producer" role.
    """
    return competitions_url\
        .subscribe_flow_as_producer(ExtractCompetitions(), as_worker=True)\
        .subscribe_flow_as_producer(ExtractDiscussions(), as_worker=True)\
        .subscribe_flow_as_producer(SearchForGHRepos(), as_worker=True)\
        .subscribe_consumer(save_gh_repo)
