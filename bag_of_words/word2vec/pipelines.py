
from .app_config import app

from .flows import SplitToSentences, SentenceToWordlist
from .consumers import fit_to_word2vec


TRAIN_WORD2VEC_CONFIG = dict(
    clean_up_sentence=SentenceToWordlist()
)


@app.pipeline(config=TRAIN_WORD2VEC_CONFIG)
def review_to_words(pipeline, review):
    return review\
        .subscribe_flow_as_generator(SplitToSentences()) \
        .subscribe_flow(pipeline.config.clean_up_sentence)


@app.pipeline()
def train_word2vec(pipeline, review):
    return review\
        .subscribe_pipeline(review_to_words)\
        .subscribe_output(fit_to_word2vec)



