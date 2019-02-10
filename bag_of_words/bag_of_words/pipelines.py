
from .app_config import app

from word2vec.consumers import fit_to_word2vec
from bag_of_words.utils import words_to_centroids
from bag_of_words.consumers import fit_to_bag_of_words

from bag_of_words.flows import SplitToSentences, SentenceToWordlist


TRAIN_WORD2VEC_CONFIG = dict(
    clean_up_sentence=SentenceToWordlist()
)


@app.pipeline(config=TRAIN_WORD2VEC_CONFIG)
def review_to_words(pipeline, review):
    return review\
        .subscribe_flow_as_producer(SplitToSentences()) \
        .subscribe_flow(pipeline.config['clean_up_sentence'])


@app.pipeline()
def train_bag_of_words(pipeline, review):
    return review\
        .subscribe_pipeline(review_to_words)\
        .subscribe_func(words_to_centroids)\
        .subscribe_consumer(fit_to_bag_of_words)


@app.pipeline(config=dict(preparing_data=review_to_words))
def fit_data_to_word2vec(pipeline, review):
    return review\
        .subscribe_pipeline(pipeline.config['preparing_data'])\
        .subscribe_consumer(fit_to_word2vec)
