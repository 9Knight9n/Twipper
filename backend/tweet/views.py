import pickle
from datetime import datetime,timedelta
from collections import Counter
import numpy as np
import pandas as pd
import math
import nltk
import pytz
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from operator import add
from scripts import TFIDFExtractor
from scripts.LDAExtractor import LDA, percentage_results, create_and_save_model,\
    save_topics, save_user_topics
from scripts.ARIMA import arima_forecast, find_best_arima
# from scripts.Trend.TrendPrediction import train
from scripts.Trend.Trend import save_all_trends_by_place, save_trends_tweet, save_places
from scripts.Trend.TrendPrediction import train
from scripts.User import get_user_by_username
from scripts.Tweet import get_user_tweets, save_collection_tweets, extract_trend_tweets
from tweet.models import TwitterUser, Collection, CollectionTwitterUser, FetchedInterval, Tweet, \
    TrendOccurrence, UserTopic, LDATopic, UserTopicARIMA, Trend, Place,Trend_TABLEDATA
from twipper.config import OLDEST_TWEET_DATE, FETCH_INTERVAL_DURATION, LDA_SAVE_LOCATION, NEWEST_TWEET_DATE
from scripts.Trend.config import HEADER, ARCHIVE_BASE_URL, OLDEST_TREND_DATE, NEWEST_TREND_DATE

import after_response


def index(request):
    return HttpResponse("Hello, world. You're at the Twipper index.")

class CollectionApiView(APIView):
    def get(self, request, *args, **kwargs):
        collections = Collection.objects.all().values('name','id')
        return Response(collections, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        collection = Collection.objects.create(name=request.data.get('name'))
        collection_twitter_user = []
        for twitter_user in request.data.get('twitter_usernames'):
            twitter_user_obj = TwitterUser.objects.get(username=twitter_user)
            collection_twitter_user.append(CollectionTwitterUser(twitter_user=twitter_user_obj,collection=collection))
        CollectionTwitterUser.objects.bulk_create(collection_twitter_user)

        save_collection_tweets.after_response(collection)

        return Response({'id':collection.id}, status=status.HTTP_201_CREATED)


class CollectionIdApiView(APIView):
    def get(self, request, collection_id, *args, **kwargs):
        max_interval = int((NEWEST_TWEET_DATE - OLDEST_TWEET_DATE).days)//int(FETCH_INTERVAL_DURATION.days)
        collection = Collection.objects.get(id=collection_id)
        # if collection.status != 'in progress':
        #     save_collection_tweets.after_response(collection)
        #     collection.status = 'in progress'
        #     collection.save()

        collection_twitter_user = CollectionTwitterUser.objects.filter(collection=collection).values('twitter_user__username','twitter_user__id')
        twitter_user_percentage = []
        for user in collection_twitter_user:
            intervals = FetchedInterval.objects.filter(twitter_user_id=user['twitter_user__id'],
                                                       complete=True).count()
            twitter_user_percentage.append({
                'name':user['twitter_user__username'],
                'progress':min([100,int((intervals/max_interval)*100)])
            })
        data = {
            'name':collection.name,
            'twitter_user_percentage':twitter_user_percentage,
            # 'done':all([item['progress'] == 100 for item in twitter_user_percentage])
            'done': True
        }
        return Response(data, status=status.HTTP_200_OK)


class TwitterUserIdApiView(APIView):

    def get(self, request, twitter_user_username, *args, **kwargs):
        user_obj = get_user_by_username(twitter_user_username)
        if not isinstance(user_obj, str):
            return Response('valid username', status=status.HTTP_200_OK)
        else:
            return Response('invalid username', status=status.HTTP_204_NO_CONTENT)


def get_users_by_collection(request, collection_id):
    collection = Collection.objects.get(id=collection_id)
    collection_twitter_user = CollectionTwitterUser.objects.filter(collection=collection).values('twitter_user__display_name','twitter_user__username','twitter_user__id','twitter_user__profile_image_url')
    twitter_user_list = []
    for user in collection_twitter_user:
        twitter_user_list.append({
            'id': user['twitter_user__id'],
            'username': user['twitter_user__username'],
            'display_name': user['twitter_user__display_name'] if user['twitter_user__display_name'] is not None
                                                                else user['twitter_user__username'],
            'avatar':user['twitter_user__profile_image_url']
        })
    data = {'name': collection.name,'twitter_user_list': twitter_user_list}
    return JsonResponse(data, status=status.HTTP_200_OK)


def get_user_info_by_id(request, user_id):
    user = TwitterUser.objects.get(id=user_id)
    user_dict = model_to_dict(user,fields=[
        'username','id','display_name','description','verified','created','followers_count','friends_count',
        'statuses_count','favourites_count','location','profile_image_url'
    ])
    return JsonResponse(user_dict, status=status.HTTP_200_OK)


def get_user_tweet_count_chart1_by_id(request, user_id,interval):
    tweets = Tweet.objects.filter(twitter_user__id=user_id).values('date')
    intervals = []
    date = Tweet.objects.filter(twitter_user__id=user_id).order_by('-date')
    if date.count() == 0:
        return JsonResponse({'data':[]}, status=status.HTTP_200_OK)
    date = date[0].date
    OLDEST_TWEET_DATE_NATIVE = OLDEST_TWEET_DATE.replace(tzinfo=pytz.UTC)
    while date >= OLDEST_TWEET_DATE_NATIVE:
        new_date = date - timedelta(days=interval)
        mid_date = date - timedelta(days=interval)/2
        intervals.append(
            {
                'x':mid_date.strftime('%d %b'),
                'z':date.strftime('%d %b')+new_date.strftime(' - %d %b'),
                'range':(new_date,date),
                'y':0
            }
        )
        date = new_date
    for tweet in tweets:
        for interval_item in intervals:
            if interval_item['range'][0] < tweet['date'] < interval_item['range'][1]:
                interval_item['y'] += 1
                break

    return JsonResponse({'data':[{'x':interval_item['x'],'y':interval_item['y'],'z':interval_item['z']} for interval_item in intervals]}, status=status.HTTP_200_OK)


def get_user_tweet_count_chart2_by_id(request, user_id,interval):
    tweets = Tweet.objects.filter(twitter_user__id=user_id).values('date')
    if interval == 7:
        intervals = {
            5:{'x':'شنبه','y':0,'z':'شنبه ها'},
            6:{'x': 'یک شنبه','y': 0,'z': 'یک شنبه ها'},
            0:{'x': 'دوشنبه','y': 0,'z': 'دوشنبه ها'},
            1:{'x': 'سه شنبه','y': 0,'z': 'سه شنبه ها'},
            2:{'x': 'چهارشنبه','y': 0,'z': 'چهارشنبه ها'},
            3:{'x': 'پنج شنبه','y': 0,'z': 'پنج شنبه ها'},
            4:{'x': 'جمعه','y': 0,'z': 'جمعه ها'},
        }
    else:
        intervals = {i:{'x':str(i),'y':0,'z':f'ساعت {i}'} for i in range(24)}
    if tweets.count() == 0:
        return JsonResponse({'data':[]}, status=status.HTTP_200_OK)
    for tweet in tweets:
        if interval == 7:
            intervals[tweet['date'].weekday()]['y'] += 1
        else:
            intervals[tweet['date'].hour]['y'] += 1
    return JsonResponse({'data':[{'x':intervals[key]['x'],'y':intervals[key]['y'],'z':intervals[key]['z']} for key in intervals.keys()]}, status=status.HTTP_200_OK)


def get_user_TF_chart1_by_id(request, user_id, start_date, stop_date):
    start_date = datetime.strptime(start_date+" 00:00:00", '%d-%m-%y %H:%M:%S')
    stop_date = datetime.strptime(stop_date+" 23:59:59", '%d-%m-%y %H:%M:%S')
    tweets = Tweet.objects.filter(twitter_user__id=user_id,date__gte=start_date,date__lte=stop_date).values('content')
    data, unique = TFIDFExtractor.apply(" ".join([tweet['content'] for tweet in tweets]),30)
    return JsonResponse({'data':data, 'unique':unique}, status=status.HTTP_200_OK)


def get_topic_words(topics, THRESHOLD=0.02):
    new_topics = {}
    for key, value in topics.items():
        topic = LDATopic.objects.get(name=key)
        words = topic.words
        new_key = ''
        words_topics = words.split(' + ')
        for j, topic in enumerate(words_topics):
            [n, w] = topic.split('*')
            if float(n) >= THRESHOLD or j < 3:
                new_key += w[1:-1] + '_'
            else:
                break
        new_topics[new_key[:-1]] = value
    return new_topics


def get_user_topics(user_id, interval):
    user_topic = UserTopic.objects.filter(twitter_user_id=user_id).\
        order_by('week_number', 'topic__name').values('value', 'topic__name')
    topics = {}
    for ut in user_topic:
        topic_name = ut['topic__name']
        if topic_name not in topics:
            topics[topic_name] = []
        topics[topic_name].append(ut['value'])

    if interval==30:
        for key, value in topics.items():
            temp = []
            for i in range(0, len(value), 4):
                temp.append(round(np.average(value[i:i+4]),2))
            topics[key] = temp

    return topics


def get_user_LDA_chart1_by_id(request, user_id,interval):
    topics = get_user_topics(user_id, interval)
    topics = get_topic_words(topics)
    for key in topics.keys():
        topics[key].reverse()
    return JsonResponse({'data':[{'name':str(key),'data':topics[key]} for key in topics.keys()]}, status=status.HTTP_200_OK)


def entropy(numbers):
    s = sum(numbers)
    if s>0:
        probabilities = [n/s for n in numbers]
    else:
        probabilities = [0] * len(numbers)
    etp = 0
    for p in probabilities:
        try:
            etp -= (p*math.log2(p))
        except:
            continue
    return etp


def get_user_LDA_chart2_by_id(request, user_id,interval):
    topics = get_user_topics(user_id, interval)
    topics = get_topic_words(topics)
    intervals_number = len(list(topics.values())[0])
    entropies = []
    for i in range(intervals_number):
        temp = [value[i] for value in topics.values()]
        entropies.append(round(entropy(temp),2))
    return JsonResponse({'data':[{'name':str(key),'data':topics[key]} for key in topics.keys()],
                         'entropies': [{'name': 'entropy', 'data': entropies}],
                         'entropy_avg': round(np.average(entropies),2)},
                          status=status.HTTP_200_OK)


def get_important_topics(topics, forecast_intervals=2):
    topics = get_topic_words(topics, THRESHOLD=0)
    temp_dict = {}
    for key, value in topics.items():
        forecasts = value[-forecast_intervals:]
        forecasts = [float(f) for f in forecasts]
        temp_dict[key] = max(forecasts)
    sorted_tuples = sorted(temp_dict.items(), key=lambda item: item[1], reverse=True)
    sorted_dict = {k: v for k, v in sorted_tuples}
    temp_dict = list(sorted_dict.keys())
    important_topics = temp_dict[0] + '_' + temp_dict[1]
    important_topics = important_topics.replace('_', ' _ ')
    return important_topics


def get_user_ARIMA_chart_by_id(request, user_id, interval):
    topics, train_loss, val_loss = {}, [], []
    user_arima = UserTopicARIMA.objects.filter(twitter_user_id=user_id)\
        .order_by('topic__name').values('topic__name', 'value', 'train_loss', 'val_loss')
    for ua in user_arima:
        topics[ua['topic__name']] = ua['value'].split('_')
        train_loss.append(ua["train_loss"])
        val_loss.append(ua['val_loss'])
    important_topics = get_important_topics(topics)
    topics = get_topic_words(topics)
    return JsonResponse({'data':[{'name':str(key),'data':topics[key]} for key in topics.keys()],
                         'important_topics': important_topics,
                         'train_loss':round(np.average(train_loss),2),
                         'val_loss': round(np.average(val_loss),2)},
                         status=status.HTTP_200_OK)


def topics_stability(topics):
    stabilities = []
    for key, value in topics.items():
        s = 0
        for i in range(1, len(value)):
            avg = np.average(value[:i])
            s += abs(value[i] - avg)
        stabilities.append({'name':key, 'stability': round(s,2)})
    return stabilities


def get_trends_by_date(start_date, end_date):
    all_trends = TrendOccurrence.objects.all().values('date', 'trend__name')
    trends = [t['trend__name'] for t in all_trends if start_date <= t['date'] < end_date]
    trends = list(set(trends))
    return trends



def get_collection_ARIMA_chart(request, collection_id):
    collection_users = CollectionTwitterUser.objects.filter(collection_id=collection_id).values('twitter_user_id')
    collection_topics, collection_train_loss, collection_val_loss = {}, [], []
    c = 0
    for cu in collection_users:
        user_id = cu['twitter_user_id']
        topics = {}
        user_arima = UserTopicARIMA.objects.filter(twitter_user_id=user_id) \
            .order_by('topic__name').values('topic__name', 'value', 'val_loss', 'train_loss')
        for ua in user_arima:
            topics[ua['topic__name']] = ua['value'].split('_')
            collection_train_loss.append(ua['train_loss'])
            collection_val_loss.append(ua['val_loss'])
        c += 1
        for key in topics.keys():
            value = [float(v) for v in topics[key]]
            if key not in collection_topics.keys():
                collection_topics[key] = value
            else:
                collection_topics[key] = list(map(add, collection_topics[key], value))
    for key, value in collection_topics.items():
        collection_topics[key] = [round(v/c,2) for v in value]

    last_topic_date = datetime.strptime('08-12-2022', '%m-%d-%Y')
    last_trend_date = last_topic_date + timedelta(days=1)
    trends = get_trends_by_date(last_topic_date.date(), last_trend_date.date())
    trends = ' _ '.join(trends)
    important_topics = get_important_topics(collection_topics)
    collection_topics = get_topic_words(collection_topics)
    stabilities = topics_stability(collection_topics)

    return JsonResponse({'data':[{'name':str(key),'data':collection_topics[key]} for key in collection_topics.keys()],
                         'important_topics': important_topics,
                         'stabilities': stabilities,
                         'trends': trends,
                         'train_loss': round(np.average(collection_train_loss),2),
                         'val_loss': round(np.average(collection_val_loss),2)},
                         status=status.HTTP_200_OK)


def get_table_correlation(request, collection_id):
    collection_users = CollectionTwitterUser.objects.filter(collection_id=collection_id).values('twitter_user_id')
    collection_topics, collection_train_loss, collection_val_loss = {}, {}, {}
    c = 0
    for cu in collection_users:
        user_id = cu['twitter_user_id']
        topics = {}
        user_arima = UserTopicARIMA.objects.filter(twitter_user_id=user_id) \
            .order_by('topic__name').values('topic__name', 'value', 'val_loss', 'train_loss')
        for ua in user_arima:
            topics[ua['topic__name']] = ua['value'].split('_')
            if ua['topic__name'] not in collection_train_loss.keys():
                collection_train_loss[ua['topic__name']] = []
                collection_val_loss[ua['topic__name']] = []
            collection_train_loss[ua['topic__name']].append(ua['train_loss'])
            collection_val_loss[ua['topic__name']].append(ua['val_loss'])
        c += 1
        for key in topics.keys():
            value = [float(v) for v in topics[key]]
            if key not in collection_topics.keys():
                collection_topics[key] = value
            else:
                collection_topics[key] = list(map(add, collection_topics[key], value))
    for key, value in collection_topics.items():
        collection_topics[key] = [round(v / c, 2) for v in value]


    stabilities = topics_stability(collection_topics)
    for i in range(len(stabilities)):
        stabilities[i]['train_loss'] = round(np.average(collection_train_loss[stabilities[i]['name']]),2)
        stabilities[i]['val_loss'] = round(np.average(collection_val_loss[stabilities[i]['name']]),2)

    corr = pd.DataFrame(stabilities).corr()['stability'].to_list()
    return JsonResponse({'data': stabilities,
                         'correlation': [{'name': 'stability correlation with train loss', 'value':round(corr[1],2)},
                                         {'name': 'stability correlation with valloss', 'value':round(corr[2],2)}]})



@after_response.enable
def async_func():
    f = open("files/sajad_crawl_users.txt", "r")
    users = f.read().split(',')
    f.close()
    print(users)
    total = len(users)
    for index,user in enumerate(users):
        print(f'{index} out of {total} : {round((index/total)*100,2)}')
        try:
            get_user_tweets(get_user_by_username(user))
        except Exception as e:
            print(e.__str__)


def scripts(request):
    async_func.after_response()




    # save_places()
    # trends_id = TrendOccurrence.objects.filter(date__lte=NEWEST_TREND_DATE.replace(tzinfo=pytz.UTC).date(),
    #                                         date__gte=OLDEST_TREND_DATE.replace(tzinfo=pytz.UTC).date()).\
    # values_list('trend_id',flat=True)
    # trends_id = list(trends_id)
    # trends = Trend.objects.filter(id__in=trends_id)
    # print(f'trends count:{trends.count()}')
    # tweets = Tweet.objects.filter(trend__in=trends).values('twitter_user__username','content','date','trend__name')
    # print(f'tweets count:{tweets.count()}')
    # save_all_trends_by_place(Place.objects.get(name='united-states'))
    # save_trends_tweet.after_response()
    # Trend_TABLEDATA.objects.all().delete()
    # li = []
    # for item in tweets:
    #     li.append(Trend_TABLEDATA(username = item['twitter_user__username'], text = item['content'], date = item['date'], trend = item['trend__name']))
    # Trend_TABLEDATA.objects.bulk_create(li)
    
    
    
    
    # create_and_save_model()
    # train()
    
    # import nltk
    #
    # nltk.download('stopwords')
    # nltk.download('wordnet')
    # nltk.download('omw-1.4')
    
    # print(extract_trend_tweets(Trend.objects.create(name="iran"),5))
    # collection = Collection.objects.get(id=5)
    # for i in range(100):
    #     save_collection_tweets(collection)
    # topics, last_date = get_user_topics(None, 7)
    # find_best_arima(topics, forecast_intervals=4)

    # save_topics()
    # save_user_topics(7)
    # for row in UserTopic.objects.all().reverse():
    #     if UserTopic.objects.filter(week_number=row.week_number, topic_id=row.topic_id,
    #                                 twitter_user_id=row.twitter_user_id).count() > 1:
    #         row.delete()
    #
    # twitter_users = TwitterUser.objects.all()
    # user_topic_arima = []
    # error_users = []
    # for tu in twitter_users:
    #     user_id = tu.id
    #     topics = get_user_topics(user_id, 7)
    #     try:
    #         trends_time_series, train_loss, val_loss = arima_forecast(topics, forecast_intervals=2)
    #     except:
    #         error_users.append(user_id)
    #         continue
    #     c = 0
    #     for key, value in trends_time_series.items():
    #         topic_id = LDATopic.objects.get(name=key)
    #         twitter_user = TwitterUser.objects.get(id=user_id)
    #         arima_value = '_'.join([str(v) for v in value])
    #         user_topic_arima.append(UserTopicARIMA(topic=topic_id, twitter_user=twitter_user,
    #                                                train_loss=train_loss[c], val_loss=val_loss[c],
    #                                                value=str(arima_value)))
    #         c+=1
    #     print(user_id)

    # UserTopicARIMA.objects.bulk_create(user_topic_arima)
    # print('user arima topic saved!')
    # for row in UserTopicARIMA.objects.all().reverse():
    #     if UserTopicARIMA.objects.filter(topic_id=row.topic_id,twitter_user_id=row.twitter_user_id).count() > 1:
    #         row.delete()
    # print('done with errors', error_users)
    return HttpResponse(f"done.")