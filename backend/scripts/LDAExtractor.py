import pickle
import random
import gensim.corpora as corpora
from gensim.models.ldamodel import LdaModel
from gensim.utils import simple_preprocess
import re
import nltk
from nltk.corpus import stopwords
import itertools
import after_response

from tweet.models import Tweet
from twipper.config import LDA_SAVE_LOCATION


def preprocess(text, stop_words, lemmatizer):
    text = re.sub('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', '', text)  # remove links
    text = re.sub('\S*@\S*\s?', '', text)  # remove emails
    text = re.sub('\s+', ' ', text)  # remove newline chars
    text = re.sub("\'", "", text)  # remove single quotes

    text = simple_preprocess(str(text), deacc=True)
    text = [re.sub('[^a-z]', '', word) for word in text]  # remove non english characters

    text = [word for word in text if word not in stop_words]  # remove stopwords
    text = [word for word in text if len(word) > 2]  # remove short words
    # text = [lemmatizer.lemmatize(word) for word in text if len(word) > 1]  # lemmatize words

    return text


class LDA:
    def __init__(self,documents_texts=None, topics_number=20):
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        self.stop_words = stopwords.words('english')
        self.stop_words = set(self.stop_words)
        self.lemmatizer = nltk.stem.WordNetLemmatizer()
        self.create_model(documents_texts, topics_number)

    def create_model(self,documents_texts=None, topics_number=20, iterations=100):
        # Preprocess

        self.documents_words = \
            [preprocess(document_text, self.stop_words, self.lemmatizer) for document_text in documents_texts]
        self.documents_words = [words for words in self.documents_words if len(words) > 2]
        # Create Dictionary
        self.id2word = corpora.Dictionary(self.documents_words)
        # Create Corpus: Term Document Frequency
        self.corpus = [self.id2word.doc2bow(t) for t in self.documents_words]
        # Create LDA model and return that
        self.topics_number = topics_number
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

    def extract_topics(self, tweets):
        tweets_words = [preprocess(tweet,self.stop_words,self.lemmatizer) for tweet in tweets]
        tweet_words = []
        for words in tweets_words:
            tweet_words += words
        tweets_trends = []

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


def create_and_save_model():
    print('getting all tweets...')
    tweets = Tweet.objects.all().values('content')
    # random indexes for tweets
    # all_tweets, random_indexes = [], []
    # while len(random_indexes)<10000:
    #     r = random.randint(0, len(tweets))
    #     if r not in random_indexes:
    #         random_indexes.append(r)
    # for i, tweet in enumerate(tweets):
    #     if i in random_indexes:
    #         all_tweets.append(tweet['content'])
    all_tweets = [tweet['content'] for tweet in tweets]
    # create an lda class object
    print('creating model with', len(all_tweets), 'tweets ...')
    lda_model = LDA(all_tweets, 8)
    print('saving model...')
    with open(LDA_SAVE_LOCATION, 'wb') as output_addr:
        pickle.dump(lda_model, output_addr, pickle.HIGHEST_PROTOCOL)
    print('done creating LDA model.')