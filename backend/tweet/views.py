import pickle
from datetime import datetime,timedelta
from collections import Counter
import numpy as np
import math
import nltk
import pytz
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from scripts import TFIDFExtractor
from scripts.LDAExtractor import LDA, percentage_results, create_and_save_model
from scripts.ARIMA import arima_forecast, find_best_arima
from scripts.User import get_user_by_username
from scripts.Tweet import get_user_tweets, save_collection_tweets
from tweet.models import TwitterUser, Collection, CollectionTwitterUser, FetchedInterval, Tweet
from twipper.config import OLDEST_TWEET_DATE, FETCH_INTERVAL_DURATION, LDA_SAVE_LOCATION


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class CollectionApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        collections = Collection.objects.all().values('name','id')
        return Response(collections, status=status.HTTP_200_OK)

    # 2. Create
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
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # def get_object(self, todo_id, user_id):
    #     '''
    #     Helper method to get the object with given todo_id, and user_id
    #     '''
    #     try:
    #         return Todo.objects.get(id=todo_id, user = user_id)
    #     except Todo.DoesNotExist:
    #         return None

    # 3. Retrieve
    def get(self, request, collection_id, *args, **kwargs):
        max_interval = int((datetime.now() - OLDEST_TWEET_DATE).days)//int(FETCH_INTERVAL_DURATION.days)
        collection = Collection.objects.get(id=collection_id)
        # if collection.status != 'in progress':
        #     save_collection_tweets.after_response(collection)
        collection_twitter_user = CollectionTwitterUser.objects.filter(collection=collection).values('twitter_user__username','twitter_user__id')
        twitter_user_percentage = []
        for user in collection_twitter_user:
            intervals = FetchedInterval.objects.filter(twitter_user_id=user['twitter_user__id']).count()
            twitter_user_percentage.append({
                'name':user['twitter_user__username'],
                'progress':min([100,int((intervals/max_interval)*100)])
            })
        data = {
            'name':collection.name,
            'twitter_user_percentage':twitter_user_percentage,
            'done':all([item['progress'] == 100 for item in twitter_user_percentage])
        }
        return Response(data, status=status.HTTP_200_OK)

    # # 4. Update
    # def put(self, request, todo_id, *args, **kwargs):
    #     '''
    #     Updates the todo item with given todo_id if exists
    #     '''
    #     todo_instance = self.get_object(todo_id, request.user.id)
    #     if not todo_instance:
    #         return Response(
    #             {"res": "Object with todo id does not exists"},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     data = {
    #         'task': request.data.get('task'),
    #         'completed': request.data.get('completed'),
    #         'user': request.user.id
    #     }
    #     serializer = TodoSerializer(instance = todo_instance, data=data, partial = True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # # 5. Delete
    # def delete(self, request, todo_id, *args, **kwargs):
    #     '''
    #     Deletes the todo item with given todo_id if exists
    #     '''
    #     todo_instance = self.get_object(todo_id, request.user.id)
    #     if not todo_instance:
    #         return Response(
    #             {"res": "Object with todo id does not exists"},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     todo_instance.delete()
    #     return Response(
    #         {"res": "Object deleted!"},
    #         status=status.HTTP_200_OK
    #     )


class TwitterUserIdApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

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
    data = TFIDFExtractor.apply(" ".join([tweet['content'] for tweet in tweets]))
    return JsonResponse({'data':data}, status=status.HTTP_200_OK)


def get_user_topics(user_id, interval, THRESHOLD = 0.02):
    if user_id is None:
        tweets = Tweet.objects.filter().values('date', 'content')
        date = Tweet.objects.filter().order_by('-date')
    else:
        tweets = Tweet.objects.filter(twitter_user__id=user_id).values('date', 'content')
        date = Tweet.objects.filter(twitter_user__id=user_id).order_by('-date')
    'got tweets!'
    intervals = []
    if date.count() == 0:
        return JsonResponse({'data': []}, status=status.HTTP_200_OK)

    date = date[0].date
    OLDEST_TWEET_DATE_NATIVE = OLDEST_TWEET_DATE.replace(tzinfo=pytz.UTC)
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
    file = open(LDA_SAVE_LOCATION, 'rb')
    lda_model = pickle.load(file)
    file.close()

    trends = {}
    intervals.reverse()
    for interval_item in intervals:
        tweets_in_interval = []
        for tweet in tweets:
            if interval_item['range'][0] < tweet['date'] < interval_item['range'][1]:
                tweets_in_interval.append(tweet)
        top_trends = lda_model.extract_topics([tweet['content'] for tweet in tweets_in_interval])
        top_trends = percentage_results(top_trends, 8)
        for i in range(8):
            if i not in top_trends.keys():
                top_trends[i] = 0

        for i, words in lda_model.model.print_topics():
            new_key = ''
            topics = words.split(' + ')
            for j, topic in enumerate(topics):
                [n, w] = topic.split('*')
                if float(n) >= THRESHOLD or j < 3:
                    new_key += w[1:-1] + '_'
                else:
                    if new_key[:-1] not in trends.keys():
                        trends[new_key[:-1]] = []
                    trends[new_key[:-1]].append(round(top_trends[i], 2))
                    break

    return trends


def get_user_LDA_chart1_by_id(request, user_id,interval):
    topics = get_user_topics(user_id, interval)
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
    intervals_number = len(list(topics.values())[0])
    numbers = []
    for i in range(intervals_number):
        temp = [value[i] for value in topics.values()]
        numbers.append(temp.index(max(temp)))
    numbers = list(dict(Counter(numbers)).values())
    data_entropy = round(entropy(numbers),2)
    return JsonResponse({'data':[{'name':str(key),'data':topics[key]} for key in topics.keys()],
                         'entropy': data_entropy},
                        status=status.HTTP_200_OK)



def get_user_ARIMA_chart_by_id(request, user_id,interval):
    topics = get_user_topics(user_id, interval)
    print('got topics!')
    topics, important_topics, train_loss, val_loss = arima_forecast(topics, forecast_intervals=4)
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


def get_collection_ARIMA_chart(request,interval):
    topics = get_user_topics(None, interval)
    print('got topics!')
    stabilities = topics_stability(topics)
    trends, important_topics, train_loss, val_loss = arima_forecast(topics, forecast_intervals=4)
    trends = ''
    return JsonResponse({'data':[{'name':str(key),'data':topics[key]} for key in topics.keys()],
                        'important_topics': important_topics,
                        'stabilities': stabilities,
                        'trends': trends,
                         'train_loss': round(np.average(train_loss),2),
                         'val_loss': round(np.average(val_loss),2)},
                        status=status.HTTP_200_OK)



def scripts(request):
    create_and_save_model()

    # topics = get_user_topics(None, 7)
    # find_best_arima(topics, forecast_intervals=4)

    return HttpResponse(f"done.")