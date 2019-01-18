
from .app_config import app

from word2vec.pipelines import review_to_words
from bag_of_words.utils import words_to_centroids
from bag_of_words.consumers import fit_to_bag_of_words


@app.pipeline()
def train_bag_of_words(pipeline, review):
    return review\
        .subscribe_pipeline(review_to_words)\
        .subscribe_func(words_to_centroids)\
        .subscribe_consumer(fit_to_bag_of_words)

