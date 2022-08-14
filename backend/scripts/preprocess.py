import re
import string


def tweet_preprocess(text:str):
    min_length = 50
    text = text.lower().replace('&amp',' ')
    text = re.sub('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', '', text)  # remove links
    text = re.sub('\S*@\S*\s?', '', text)  # remove emails
    text = re.sub('\s+', ' ', text)  # remove newline chars
    text = re.sub("\'", "", text)  # remove single quotes
    # text = [re.sub('[^a-z]', '', word) for word in text]  # remove non english characters
    text = text.translate(str.maketrans('', '', string.punctuation))



    text = text.strip()
    if len(text) < min_length:
        return None
    return text