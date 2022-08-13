import requests
from bs4 import BeautifulSoup

from scripts.Trend import HEADER, ARCHIVE_BASE_URL
from tweet.models import Place
from datetime import date


def get_places():
    places = Place.objects.all()
    if places.count() > 0:
        return places
    f = requests.get(ARCHIVE_BASE_URL, headers=HEADER)
    soup = BeautifulSoup(f.content, 'lxml')
    places = [Place(name=place.get_text()) for place in soup.select("select#dsad option") if place.get_text() != '']
    Place.objects.bulk_create(places)
    return Place.objects.all()


def save_trends_by_date_and_place(place: Place, day: date):
    url = ARCHIVE_BASE_URL + place.name.lower() + "/" + day.strftime("%d-%m-%Y")
    print(url)
    f = requests.get(url, headers=HEADER)
    soup = BeautifulSoup(f.content, 'lxml')
    trends_name = [name.get_text() for name in soup.select("span#en_volume_b div.table_bb span.table_bbk")]
    print(soup.select("span#en_volume_b div.table_bb span.table_bbk"))
    trends_tweet_count = [name.get_text() for name in soup.select("span#en_volume_b div.table_bbv span.table_bbiv")]
    return [{'name': trends_name[index], 'count': trends_tweet_count[index]} for index in range(len(trends_name))]
