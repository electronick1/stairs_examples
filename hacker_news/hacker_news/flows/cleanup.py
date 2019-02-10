from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from keras.preprocessing.text import text_to_word_sequence

from stairs import Flow, step, StopPipelineFlag


class PrepareText(Flow):
    """
    Flow for cleaning data.
    """

    def __call__(self, text):
        """
        Data from pipeline always comes to __call__ method. And here we could
        start executing FLow.

        Each Flow has `steps` and result of each step is an input for another.
        (like a chain (tree) of functions which change your data)

        Flow it's a way to make your pipeline more scalable in case of
        changes.
        Image if you have a ton of simple steps in pipeline, and you want
        to change something. Here you can simple use class inheritance and
        change ANY pipeline steps you want.

        """
        # start's from self.extract_words step with a text value
        result = self.start_from(self.extract_words, text=text)

        # result will have data from last step or from steps with flag
        # `save_result=True`
        # See http://stairspy.com/#flow for more info.
        return result.words_data

    @step(None)
    def words_data(self, words, stemmed_words):
        """
        It's a last step and result of this step will be return as a result
        of all "chain" of steps.
        """
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
        """
        Words comes from `extract_words` step
        """
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if not w in stop_words]
        return dict(
            words=words
        )

    # `filter_stop_words` it's a next step which will be called after
    # `extract_words`.
    @step(filter_stop_words)
    def extract_words(self, text):
        # return words, which will be then send to `filter_stop_words` step
        return dict(
            words=text_to_word_sequence(text)
        )


class FilterComments(Flow):
    """
    Flow to filter no related hacker news posts
    """
    def __init__(self, topic, min_amount_of_words=5):
        """
        We can use __init__ to configure Flow object from pipeline.
        """
        self.topic = topic
        self.min_amount_of_words = min_amount_of_words

    def __call__(self, type, words):
        self.start_from(
            self.ensure_comment,
            type=type,
            words=words,
        )
        # We return empty dict because filter flow do not change data
        # it's stop whole pipeline for one item in case if it's not useful
        # for us
        return dict()

    @step(None)
    def ensure_topic_related(self, words):
        """
        We are using  StopPipelineFlag in case if we want to stop next
        processing for current item in pipeline (queue).
        """
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

