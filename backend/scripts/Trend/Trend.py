import datetime
import pickle

import after_response
import pytz
import requests
from bs4 import BeautifulSoup
from django.db.models import Sum, Max

from scripts.LDAExtractor import percentage_results
from scripts.Trend.config import HEADER, ARCHIVE_BASE_URL, OLDEST_TREND_DATE, NEWEST_TREND_DATE
from scripts.Tweet import extract_trend_tweets
from scripts.preprocess import tweet_preprocess
from tweet.models import Place, Trend, TrendOccurrence, Tweet
from datetime import date

from twipper.config import OLDEST_TWEET_DATE, LDA_SAVE_LOCATION


def save_places():
    places = Place.objects.all()
    if places.count() > 0:
        return places
    f = requests.get(ARCHIVE_BASE_URL, headers=HEADER)
    soup = BeautifulSoup(f.content, 'lxml')
    places = [Place(name=place.get_text().lower().replace(' ','-')) for place in soup.select("select#dsad option") if place.get_text() != '']
    Place.objects.bulk_create(places)
    return Place.objects.all()


def save_trends_by_date_and_place(place: Place, day: date):
    trends_of_day = TrendOccurrence.objects.filter(place=place,date=day)
    if trends_of_day.count() > 0:
        return trends_of_day
    trend_names = list(Trend.objects.all().values_list('name',flat=True))
    # print(trend_names)

    result = []
    url = ARCHIVE_BASE_URL + place.name.lower() + "/" + day.strftime("%d-%m-%Y")
    f = requests.get(url, headers=HEADER)
    soup = BeautifulSoup(f.content, 'lxml')
    time_tables = soup.select(".tek_tablo")
    for time_table in time_tables:
        try:
            time = time_table.select('.trend_baslik611')[0].get_text()
        except Exception as e:
            print(e.__str__())
            continue
        trends_tweet_name = [name.get_text() for name in time_table.select(".trend611")]
        trends_tweet_count = [count.get_text() for count in time_table.select(".trend611_s")]
        if len(trends_tweet_count) != len(trends_tweet_name):
            continue
        result += [{'name':trends_tweet_name[index],
                    'tweet_count':int(trends_tweet_count[index]) if trends_tweet_count[index] != '-' else None,
                    'time':datetime.datetime.strptime(time,'%H:%M'), 'place':place}
                   for index in range(len(trends_tweet_name))]


    new_trends = []
    for item in result:
        if item['name'] not in trend_names:
            new_trends.append(Trend(name=item['name']))
            trend_names.append(item['name'])
    Trend.objects.bulk_create(new_trends)

    trends = Trend.objects.all().values('id','name')
    trends_dict = {}
    for trend in trends:
        trends_dict[trend['name']] = trend['id']

    TrendOccurrence.objects.bulk_create([TrendOccurrence(trend_id=trends_dict[item['name']],
                                                         date=day,place=place,
                                                         tweet_count=item['tweet_count'],
                                                         time=item['time']) for item in result])

    return TrendOccurrence.objects.filter(place=place,date=day)


def save_all_trends_by_place(place: Place):
    day = NEWEST_TREND_DATE
    while day.date() > OLDEST_TREND_DATE.date():
        save_trends_by_date_and_place(place,day)
        day -= datetime.timedelta(days=1)
    return TrendOccurrence.objects.filter(place=place)


@after_response.enable
def save_trends_tweet():
    tweets = list(Tweet.objects.all().values_list('twitter_id',flat=True))
    trend_tweet_count = 1000
    trends_id = TrendOccurrence.objects.filter(date__lte=NEWEST_TREND_DATE.replace(tzinfo=pytz.UTC).date(),
                                               date__gte=OLDEST_TREND_DATE.replace(tzinfo=pytz.UTC).date()).\
        values_list('trend_id',flat=True)
    trends_id = list(trends_id)
    trends = Trend.objects.filter(id__in=trends_id)
    tweet_list = []
    bulk_limit = 1000
    c = 0
    for trend in trends:
        c += 1
        print(f'added tweets for {c} trends.')
        count = Tweet.objects.filter(trend=trend).count()
        if count >= trend_tweet_count:
            continue
        trend_text,tweets = extract_trend_tweets(trend, trend_tweet_count-count,tweets)
        if trend_text is None:
            continue
        tweet_list += trend_text
        if len(tweet_list) > bulk_limit:
            Tweet.objects.bulk_create(tweet_list)
            tweet_list = []
    Tweet.objects.bulk_create(tweet_list)

    # Trend.objects.all().update(topic=None)
    # bulk_update = []
    # update_limit = 100
    # for trend in trends:
    #     texts = Tweet.objects.filter(trend=trend).values_list('content', flat=True)
    #     text = ''
    #     for txt in texts:
    #         pre_txt = tweet_preprocess(txt)
    #         if pre_txt is not None:
    #             text += " " + pre_txt
    #     if len(text) < 100:
    #         continue
    #     trend.topic = text
    #     bulk_update.append(trend)
    #     if len(bulk_update) > update_limit:
    #         Trend.objects.bulk_update(bulk_update,['topic'])
    #         bulk_update = []
    # Trend.objects.bulk_update(bulk_update, ['topic'])
