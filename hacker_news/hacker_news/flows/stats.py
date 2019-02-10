from textblob import TextBlob
from stairs import Flow, step

# See `cleanup` flow if you want to know basic information about Flow components


class CalculateSentiment(Flow):
    """
    Flow to calculate sentiment values.
    """
    def __call__(self, text):
        result = self.start_from(self.make_blob, text=text)
        return result.average_sentiment

    @step(None)
    def average_sentiment(self, by_sentences):
        return dict(
            sentiment=sum(by_sentences) / len(by_sentences)
        )

    @step(average_sentiment)
    def extract_sentiment(self, blob):
        by_sentences = [sentence.sentiment.polarity for sentence in blob.sentences]
        return dict(by_sentences=by_sentences)

    @step(extract_sentiment)
    def make_blob(self, text):
        return dict(blob=TextBlob(text))


class CalculateMentionedLibs(Flow):
    """
    Flow to calculate mentions of some libs in hacker_news posts.
    """

    SCORE_INTERVALS = {
        'null': 1,
        'low': 3,
        'premiddle': 5,
        'middle': 10,
        'high': 25,
        'awesome': 50,
        'god': 10**6,
    }

    def __init__(self, libs_list=None):
        if libs_list is None:
            self.libs_list = []
        else:
            self.libs_list = libs_list

    def __call__(self, score, time, words):
        libs_info = []

        for word in words:
            if word in self.libs_list:
                libs_info.append([word, score, time])

        return dict(libs=libs_info)
