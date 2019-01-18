from .app_config import app


@app.consumer_iter()
def fit_to_bag_of_words(**data):
    return data
