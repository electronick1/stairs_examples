from .app_config import app


@app.consumer_iter()
def fit_to_word2vec(words):
    return words


