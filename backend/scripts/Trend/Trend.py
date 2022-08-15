import datetime
import pickle

import requests
from bs4 import BeautifulSoup

from scripts.LDAExtractor import percentage_results
from scripts.Trend import HEADER, ARCHIVE_BASE_URL
from scripts.Tweet import extract_trend_tweets
from tweet.models import Place, Trend, TrendOccurrence
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
    day = datetime.date.today() - datetime.timedelta(days=1)
    while day > OLDEST_TWEET_DATE.date():
        save_trends_by_date_and_place(place,day)
        day -= datetime.timedelta(days=1)
    return TrendOccurrence.objects.filter(place=place)


def save_trends_topic():
    trends = Trend.objects.filter(topic__isnull=True)
    file = open(LDA_SAVE_LOCATION, 'rb')
    lda_model = pickle.load(file)
    file.close()
    update_trend = []
    bulk_limit = 50
    for trend in trends:
        trend_text = extract_trend_tweets(trend, 10)
        if trend_text is None:
            continue
        top_trends = lda_model.extract_topics(trend_text)
        top_trends = percentage_results(top_trends, 8)
        trend.topic = top_trends
        update_trend.append(trend)
        if len(update_trend) > bulk_limit:
            Trend.objects.bulk_update(update_trend,['topic'])
            update_trend = []
            print('added some')
    Trend.objects.bulk_update(update_trend,['topic'])

