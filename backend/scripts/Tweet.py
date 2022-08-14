import snscrape.modules.twitter as sntwitter
from datetime import datetime, timedelta
import after_response

from scripts.preprocess import tweet_preprocess
from tweet.models import TwitterUser, FetchedInterval, Tweet, CollectionTwitterUser, Trend
from twipper.config import OLDEST_TWEET_DATE, FETCH_INTERVAL_DURATION


def _get_delta_time_before(date_time: datetime):
    date = date_time.replace(hour=0, minute=0, second=0, microsecond=0)
    delta_date = []
    if not _datetime_equal(date, date_time):
        delta_date.append((date, date_time))
    while date > OLDEST_TWEET_DATE:
        new_date = date - FETCH_INTERVAL_DURATION
        delta_date.append((new_date, date))
        date = new_date
    return delta_date


def _get_delta_time_after(date_time: datetime):
    date = date_time.replace(hour=0, minute=0, second=0, microsecond=0)
    now = datetime.now()
    delta_date = []
    while date < now:
        new_date = date + FETCH_INTERVAL_DURATION
        delta_date.append((date, min([new_date,now])))
        date = new_date
    return delta_date


def _datetime_equal(datetime1:datetime,datetime2:datetime):
    big = max([datetime1,datetime2])
    small = min([datetime1,datetime2])
    return big-small < timedelta(seconds=1)


def _remove_interval_from_list(list_:list,interval:tuple):
    index = -1
    for i,item in enumerate(list_):
        if _datetime_equal(item[0],interval[0]) and _datetime_equal(item[1],interval[1]):
            index = i
            break
    if index != -1:
        return [ item for i,item in enumerate(list_) if i != index]
    return list_

def extract_user_tweets(user:TwitterUser,interval:tuple):
    fetched_interval = FetchedInterval.objects.create(twitter_user=user,
        interval_start=interval[0],
        complete=_datetime_equal(interval[0] + FETCH_INTERVAL_DURATION, interval[1]))
    tweets_list = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(
            f'from:{user.username} '
            f'since:{interval[0].strftime("%Y-%m-%d")} '
            f'until:{interval[1].strftime("%Y-%m-%d")}').get_items()):
        tweets_list.append(Tweet(
            twitter_user = user,
            twitter_id = tweet.id,
            url = tweet.url,
            date = tweet.date,
            content = tweet.content,
            reply_count = tweet.replyCount,
            retweet_count = tweet.retweetCount,
            like_count = tweet.likeCount,
            quote_count = tweet.quoteCount,
            twitter_conversation_id = tweet.conversationId,
            lang = tweet.lang,
            sourceLabel = tweet.sourceLabel,
            tweeter_in_reply_to_tweet_id = tweet.inReplyToTweetId,
            # longitude = tweet.place.longitude if tweet.place and tweet.place.longitude else None,
            # latitude = tweet.place.latitude if tweet.place and tweet.place.latitude else None,
            fetched_interval = fetched_interval,
        ))
    return tweets_list


def get_user_tweets(user:TwitterUser):
    Tweet.objects.filter(twitter_user=user,fetched_interval__complete=False).delete()
    FetchedInterval.objects.filter(twitter_user=user,complete=False).delete()
    fetched_intervals = FetchedInterval.objects.filter(twitter_user=user).order_by('-interval_start')\
        .values('interval_start','id')
    if len(fetched_intervals) == 0:
        intervals = _get_delta_time_before(datetime.now())
    else:
        interval_start_example = datetime.combine(fetched_intervals[0]['interval_start'], datetime.min.time())
        intervals = _get_delta_time_before(interval_start_example) + _get_delta_time_after(interval_start_example)
        for fetched_interval in fetched_intervals:
            interval_start = datetime.combine(fetched_interval['interval_start'], datetime.min.time())
            intervals = _remove_interval_from_list(intervals,(interval_start,interval_start+FETCH_INTERVAL_DURATION))

    for interval in intervals:
        tweets_list = extract_user_tweets(user,interval)
        try:
            Tweet.objects.bulk_create(tweets_list)
        except Exception as e:
            print("error in bulk request.")
            print('trying to save one by one.')
            for obj in tweets_list:
                try:
                    obj.save()
                except Exception as e:
                    print(f'error in save of {obj}')
                    print(e.__str__())
                    continue

    return Tweet.objects.filter(twitter_user=user)


@after_response.enable
def save_collection_tweets(collection):
    collection.status = 'in progress'
    collection.save()
    users_id = CollectionTwitterUser.objects.filter(collection=collection).values('twitter_user__id')
    users = TwitterUser.objects.filter(id__in=[user_id['twitter_user__id'] for user_id in users_id])
    for user in users:
        get_user_tweets(user).count()
    collection.status = 'done'
    collection.save()


def extract_trend_tweets(trend:Trend,top:int):
    tweets_list = []
    found_all = False
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query='"'+trend.name+'"'+" lang:en min_retweets:100")
                                      .get_items()):
        tweet_text = tweet_preprocess(tweet.content)
        if tweet_text is None:
            continue
        tweets_list.append(tweet_text)
        if len(tweets_list) == top:
            found_all = True
            break
    if not found_all:
        return None
    return tweets_list