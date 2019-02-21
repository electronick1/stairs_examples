from .app_config import app
from . import pipelines

KAGGLE_COMPETITIONS_PAGE = "https://www.kaggle.com/competitions"


@app.producer(pipelines.parse_gh_repos)
def start_kaggle_parsing():
    yield dict(competitions_url=KAGGLE_COMPETITIONS_PAGE)
