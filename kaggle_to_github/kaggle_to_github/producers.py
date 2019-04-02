from .app_config import app
from . import pipelines

KAGGLE_COMPETITIONS_PAGE = "https://www.kaggle.com/competitions.json"


@app.producer(pipelines.parse_mentions)
def start_kaggle_parsing():
    for page in range(app.config.cnt_competition_pages):
        yield dict(competitions_url="%s?page=%s&pageSize=1000" %
                                    (app.config.kaggle_competition_page, page))
