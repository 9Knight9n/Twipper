import re
import string

from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def convert_hashtag(text:str):
    text = text.replace("_"," ")
    if not text.startswith('#'):
        return text.lower()
    result = ''
    for i in range(len(text)):
        ch = text[i]
        if ch.isupper() or ch.isdigit():
            if i-1 > 0 and text[i-1].isupper():
                continue
            result += ' '
        is_digit = False
        while ch.isdigit() and i < len(text) - 1:
            is_digit = True
            i += 1
            ch = text[i]
            result += ch
        if is_digit:
            result += ' '
        else:
            result += ch
    return result.lower().replace("  "," ")


def tweet_preprocess(text:str):
    min_length = 10
    text = text.replace('&amp',' ')
    text = re.sub('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', '', text)  # remove links
    text = re.sub('\S*@\S*\s?', '', text)  # remove emails
    text = re.sub('\s+', ' ', text)  # remove newline chars
    text = simple_preprocess(str(text), deacc=True)
    text = [convert_hashtag(word) for word in text]
    text = [re.sub('[^ a-z\d]', '', word.strip()) for word in text]  # remove non english characters
    stop_words = stopwords.words('english')
    text = [word for word in text if word not in stop_words]  # remove stopwords
    text = [word for word in text if len(word) > 2]  # remove short words
    lemmatizer = WordNetLemmatizer()
    text = [lemmatizer.lemmatize(word) for word in text if len(word) > 1]
    text = ' '.join(text)
    if len(text) < min_length:
        return None
    return text


def trend_preprocess(text:str):
    min_length = 3
    text = text.replace('&amp',' ')
    text = convert_hashtag(text)
    text = re.sub('[^ a-z\d]', '', text).strip()  # remove non english characters
    if len(text) < min_length:
        return '#####'
    return text