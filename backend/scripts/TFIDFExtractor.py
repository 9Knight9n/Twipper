import re
import time
import heapq
from operator import itemgetter
# from stop_words import get_stop_words
from gensim.parsing.preprocessing import remove_stopwords

from scripts.utils import remove_punctuation


def calculate_words_frequency(word_list):
    words_frequency_dict = {}
    for word in word_list:
        if word not in words_frequency_dict:
            words_frequency_dict[word] = 1
        else:
            words_frequency_dict[word] += 1
    return words_frequency_dict


def extract_tf_weight(words_frequency_dict, top):
    sum_value = sum(words_frequency_dict.values())

    top_items = heapq.nlargest(top, words_frequency_dict.items(), key=itemgetter(1))
    words_frequency_dict_sorted = dict(top_items)

    result = []
    sum_frequency = 0
    for word, term_frequency in words_frequency_dict_sorted.items():
        round_weight = round((term_frequency / sum_value) * 100, 2)
        sum_frequency += term_frequency
        result.append({'x': word, 'y': round_weight, 'z': term_frequency})
    # result.append({'x':'باقی کلمات','y':round(1-(sum_frequency/sum_value),2)*100,'z':sum_value-sum_frequency})
    return result


def apply(tweet: str, top: int):
    t = time.time()
    # print(tweet)
    tweet = preprocess(tweet)

    # print(tweet.split())

    words_frequency_dict = calculate_words_frequency(tweet.split())
    results = extract_tf_weight(words_frequency_dict, top)

    # print(results)

    print("time ", time.time() - t)
    return results, len(words_frequency_dict.keys())


def preprocess(tweet: str):
    tweet = tweet.lower()
    tweet = re.sub(r'http\S+', ' ', tweet)
    # stop_words = get_stop_words('en')
    # for stop_word in stop_words:
    #     tweet = tweet.replace(" "+stop_word+" "," ")
    tweet = remove_stopwords(tweet)
    tweet = tweet.replace("\n", " ").replace("  ", " ")
    tweet = remove_punctuation(tweet)
    return tweet
