
from .app_config import app

from .flows import ExtractCompetitions, ExtractDiscussions, SearchForGHRepos
from .consumers import save_gh_repo


@app.pipeline()
def parse_gh_repos(pipeline, competitions_url):
    return competitions_url\
        .subscribe_flow_as_producer(ExtractCompetitions())\
        .subscribe_flow_as_producer(ExtractDiscussions())\
        .subscribe_flow_as_producer(SearchForGHRepos())\
        .subscribe_consumer(save_gh_repo)
