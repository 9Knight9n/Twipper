import gensim.corpora as corpora
from gensim.models.ldamodel import LdaModel
from gensim.utils import simple_preprocess
# from gensim.models import Phrases
# from gensim.models.phrases import Phraser
import json
import pandas as pd
import re
# from spacy import load
import nltk
from nltk.corpus import stopwords
import itertools

# NLTK Stop words
nltk.download('stopwords')
stop_words = stopwords.words('english')
stop_words = set(stop_words)
lemmatizer = nltk.stem.WordNetLemmatizer()


def preprocess(text, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    text = re.sub('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', '', text)  # remove links
    text = re.sub('\S*@\S*\s?', '', text)  # remove emails
    text = re.sub('\s+', ' ', text)  # remove newline chars
    text = re.sub("\'", "", text)  # remove single quotes

    text = simple_preprocess(str(text), deacc=True)
    text = [re.sub('[^a-z]', '', word) for word in text]    # remove non english characters

    text = [word for word in text if word not in stop_words]  # remove stopwords
    text = [lemmatizer.lemmatize(word) for word in text if len(word) > 1]  # lemmatize words

    # Build the bigram and trigram models
    # bigram = Phrases(text, min_count=5, threshold=100)  # higher threshold fewer phrases.
    # trigram = Phrases(bigram[text], threshold=100)
    # bigram_mod = Phraser(bigram)
    # trigram_mod = Phraser(trigram)
    #
    # """Remove Stopwords, Form Bigrams, Trigrams and Lemmatization"""
    # texts = [word for word in text if word not in stop_words]
    # texts = [bigram_mod[doc] for doc in texts]
    # texts = [trigram_mod[bigram_mod[doc]] for doc in texts]
    # texts_out = []
    # nlp = load('en_core_web_sm', disable=['parser', 'ner'])
    # for sent in texts:
    #     doc = nlp(" ".join(sent))
    #     texts_out = [token.lemma_ for token in doc if token.pos_ in allowed_postags]
    # # remove stopwords once more after lemmatization
    # texts_out = [word for word in texts_out if word not in stop_words]
    return text


class LDA:
    def __init__(self, documents_texts, topics_number):
        # Preprocess
        self.documents_words = [preprocess(document_text) for document_text in documents_texts]
        self.documents_words = [words for words in self.documents_words if len(words) > 2]
        # Create Dictionary
        self.id2word = corpora.Dictionary(self.documents_words)
        # Create Corpus: Term Document Frequency
        self.corpus = [self.id2word.doc2bow(t) for t in self.documents_words]
        # Create LDA model and return that
        self.topics_number = topics_number
        self.create_model()

    def create_model(self, iterations=100):
        self.model = LdaModel(corpus=self.corpus,
                              id2word=self.id2word,
                              num_topics=self.topics_number,
                              random_state=100,
                              update_every=1,
                              chunksize=10,
                              passes=10,
                              alpha='symmetric',
                              iterations=iterations,
                              per_word_topics=True)

    def extract_trends(self, tweets):
        tweets_words = [preprocess(tweet) for tweet in tweets]
        tweets_trends = []
        for tweet_words in tweets_words:
            new_text_corpus = self.id2word.doc2bow(tweet_words)
            trend = self.model[new_text_corpus]
            trend[0].sort(key=lambda a: a[1], reverse=True)
            trend = trend[0]
            tweets_trends.append(trend)
        return tweets_trends


def percentage_results(tweets_trends, pick_first=5):
    percentages = {}
    for tweet_trends in tweets_trends:
        for trend, value in tweet_trends:
            try:
                percentages[trend] += value
            except:
                percentages[trend] = value

    s = sum(percentages.values())
    for k, v in percentages.items():
        pct = v * 100.0 / s
        percentages[k] = pct
    # sort dictionary
    percentages = dict(sorted(percentages.items(), key=lambda item: item[1], reverse=True))
    # select must matched trends
    first_items = dict(itertools.islice(percentages.items(), pick_first))
    return first_items


if __name__ == '__main__':
    # load json file and store tweets as a list
    f = open('tweet_tweet.json')
    data = json.load(f)
    data_df = pd.DataFrame(data[2]['data'])
    all_tweets = data_df['content'].tolist()
    # create an lda class object
    lda_model = LDA(all_tweets, 20)
    print('lda model created!')
    trends = lda_model.extract_trends(all_tweets[100:110])
    print(percentage_results(trends))
