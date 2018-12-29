from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from keras.preprocessing.text import text_to_word_sequence

from stairs import Flow, step, StopPipelineFlag


class PrepareText(Flow):

    def __call__(self, text):
        result = self.start_from(self.extract_words, text=text)

        return result.words_data

    @step(None)
    def words_data(self, words, stemmed_words):
        return dict(
            words=words,
            stemmed_words=stemmed_words
        )

    @step(words_data)
    def apply_steming(self, words):
        porter = PorterStemmer()
        return dict(
            stemmed_words=[porter.stem(word) for word in words]
        )

    @step(apply_steming)
    def filter_stop_words(self, words):
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if not w in stop_words]
        return dict(words=words)

    @step(filter_stop_words)
    def extract_words(self, text):
        return dict(
            words=text_to_word_sequence(text)
        )


class FilterComments(Flow):

    def __init__(self, topic, min_amount_of_words=5):
        self.topic = topic
        self.min_amount_of_words = min_amount_of_words

    def __call__(self, type, words):
        self.start_from(
            self.ensure_comment,
            type=type,
            words=words,
        )

    @step(None)
    def ensure_topic_related(self, words):
        if self.topic not in words:
            raise StopPipelineFlag("Is not topic related")

    @step(ensure_topic_related)
    def ensure_length_ok(self, words):
        if len(words) < self.min_amount_of_words:
            raise StopPipelineFlag("Comment too short")

    @step(ensure_length_ok)
    def ensure_comment(self, type):
        if type != "comment":
            raise StopPipelineFlag("It's not a comment")

