from .app_config import app


@app.consumer()
def save_gh_repo(c_title, gh_url):
    print(c_title, gh_url)
