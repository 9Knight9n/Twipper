import pickle
import random
import pytz
import gensim.corpora as corpora
from gensim.models.ldamodel import LdaModel
from gensim.utils import simple_preprocess
import re
import nltk
from nltk.corpus import stopwords
import itertools
from datetime import datetime,timedelta
from tweet.models import Tweet, LDATopic, UserTopic, TwitterUser
from twipper.config import LDA_SAVE_LOCATION, OLDEST_TWEET_DATE


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


def save_topics():
    file = open(LDA_SAVE_LOCATION, 'rb')
    lda_model = pickle.load(file)
    file.close()
    topics = []
    for i, words in lda_model.model.print_topics():
        topics.append(LDATopic(name=str(i), words=str(words)))
    LDATopic.objects.bulk_create(topics)
    print('all topics saved!')


def save_user_topics(interval):
    print('in save user topics ...')
    user_trends = []

    file = open(LDA_SAVE_LOCATION, 'rb')
    lda_model = pickle.load(file)
    file.close()

    twitter_users = TwitterUser.objects.all()
    for tu in twitter_users:
        user_id = tu.id
        tweets = Tweet.objects.filter(twitter_user__id=user_id).values('date', 'content')
        date = Tweet.objects.filter(twitter_user__id=user_id).order_by('-date')

        if date.count() == 0:
            break

        date = date[0].date
        OLDEST_TWEET_DATE_NATIVE = OLDEST_TWEET_DATE.replace(tzinfo=pytz.UTC)
        intervals = []
        while date >= OLDEST_TWEET_DATE_NATIVE:
            new_date = date - timedelta(days=interval)
            mid_date = date - timedelta(days=interval) / 2
            intervals.append(
                {
                    'x': mid_date.strftime('%d %b'),
                    'z': date.strftime('%d %b') + new_date.strftime(' - %d %b'),
                    'range': (new_date, date),
                    # 'y':0
                }
            )
            date = new_date

        intervals.reverse()
        for i, interval_item in enumerate(intervals):
            tweets_in_interval = []
            for tweet in tweets:
                if interval_item['range'][0] < tweet['date'] < interval_item['range'][1]:
                    tweets_in_interval.append(tweet)
            top_trends = lda_model.extract_topics([tweet['content'] for tweet in tweets_in_interval])
            top_trends = percentage_results(top_trends, 8)
            for j in range(8):
                if j not in top_trends.keys():
                    top_trends[j] = 0

            for key,value in top_trends.items():
                topic_id = LDATopic.objects.get(name=key)
                twitter_user = TwitterUser.objects.get(id=user_id)
                user_trends.append(UserTopic(week_number=i+1, topic=topic_id, twitter_user=twitter_user, value=round(value,2)))

    UserTopic.objects.bulk_create(user_trends)
    print('user topics saved!')
