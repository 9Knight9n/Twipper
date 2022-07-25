from django.http import HttpResponse

from scripts.User import get_user_by_username
from scripts.Tweet import get_user_tweets
from tweet.models import TwitterUser


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def scripts(request):
    user = get_user_by_username('khamenei_ir')
    result = get_user_tweets(user)
    for item in result:
        print(item)
    return HttpResponse(f"done extracting {result.count()} tweets.")