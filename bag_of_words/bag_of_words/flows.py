import nltk
import re

from bs4 import BeautifulSoup
from stairs.core.flow import Flow, step
from nltk.corpus import stopwords


class SplitToSentences(Flow):

    def __init__(self):
        self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    def __call__(self, review):
        r = self.start_from(self.cleanup_review,
                            review=review)

        for sentence in r.validate_sentences.raw_sentences:
            yield dict(sentence=sentence)

    @step(None)
    def validate_sentences(self, raw_sentences):
        sentences = [s for s in raw_sentences if len(s) > 1]
        return dict(raw_sentences=sentences)

    @step(validate_sentences)
    def split_paragraph_to_sentences(self, review):
        # 1. Use the NLTK tokenizer to split the paragraph into sentences
        raw_sentences = self.tokenizer.tokenize(review)
        return dict(raw_sentences=raw_sentences)

    @step(split_paragraph_to_sentences)
    def cleanup_review(self, review):
        return dict(review=review.decode('utf8').strip())


class SentenceToWordlist(Flow):

    def __init__(self, needs_stopwords=False):
        self.needs_stopwords = needs_stopwords

    def __call__(self, sentence):
        r = self.start_from(self.apply_beautiful_soup, sentence=sentence)

        return dict(words=r.remove_stopwords.words)

    @step(None)
    def remove_stopwords(self, words):
        # 4. Optionally remove stop words (false by default)
        if not self.needs_stopwords:
            stops = set(stopwords.words("english"))
            words = [w for w in words if not w in stops]

        return dict(words=words)

    @step(remove_stopwords)
    def split_by_words(self, review_text):
        # 2. Remove non-letters
        review_text = re.sub("[^a-zA-Z]", " ", review_text)
        #
        # 3. Convert words to lower case and split them
        words = review_text.lower().split()

        return dict(words=words)

    @step(split_by_words)
    def apply_beautiful_soup(self, sentence):
        # Function to convert a document to a sequence of words,
        # optionally removing stop words.  Returns a list of words.
        #
        # 1. Remove HTML
        review_text = BeautifulSoup(sentence).get_text()

        return dict(review_text=review_text)
