from .app_config import app


@app.consumer()
def save_gh_repo(c_title, gh_url, **kwargs):
    print(c_title, gh_url)
