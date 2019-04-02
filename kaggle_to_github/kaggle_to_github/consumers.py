import datetime
import redis
from .app_config import app

r = redis.Redis()


@app.consumer()
def save_gh_repo(c_title, gh_url, **kwargs):
    print(c_title, gh_url)


@app.consumer()
def aggregate_monthly(key, date, has_action, **kwargs):
    if date is None:
        return
    if isinstance(date, int):
        date = datetime.datetime.utcfromtimestamp(date)
    date = date - datetime.timedelta(days=date.day - 1)

    if int(has_action) > 0:
        r.hincrby(key, "%s-%s" % (date.date().year, date.date().month), 1)

    r.hincrby(key, "total:%s-%s" % (date.date().year, date.date().month), 1)

