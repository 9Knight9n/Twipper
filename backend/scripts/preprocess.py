import re
import string

from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def tweet_preprocess(text:str):
    min_length = 10
    text = text.lower().replace('&amp',' ')
    text = re.sub('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', '', text)  # remove links
    text = re.sub('\S*@\S*\s?', '', text)  # remove emails
    text = re.sub('\s+', ' ', text)  # remove newline chars
    text = re.sub("\'", "", text)  # remove single quotes
    # text = [re.sub('[^a-z]', '', word) for word in text]  # remove non english characters
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = simple_preprocess(str(text), deacc=True)
    text = [re.sub('[^a-z]', '', word.strip()) for word in text]  # remove non english characters
    stop_words = stopwords.words('english')
    text = [word for word in text if word not in stop_words]  # remove stopwords
    text = [word for word in text if len(word) > 2]  # remove short words
    lemmatizer = WordNetLemmatizer()
    text = [lemmatizer.lemmatize(word) for word in text if len(word) > 1]
    text = ' '.join(text)
    if len(text) < min_length:
        return None
    return text