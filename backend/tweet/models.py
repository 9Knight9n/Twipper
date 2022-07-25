from django.db import models


class TwitterUser(models.Model):
    username = models.CharField(max_length=16,unique=True)
    id = models.AutoField(primary_key=True)
    # twitter_id = models.IntegerField(unique=True)
    display_name = models.CharField(max_length=50,null=True)
    description = models.TextField(null=True)
    verified = models.BooleanField(null=True)
    created = models.DateField(null=True)
    followers_count = models.IntegerField(null=True)
    friends_count = models.IntegerField(null=True)
    statuses_count = models.IntegerField(null=True)
    favourites_count = models.IntegerField(null=True)
    location = models.CharField(max_length=50,null=True)
    protected = models.BooleanField(null=True)
    profile_image_url = models.CharField(max_length=256,null=True)
    profile_banner_url = models.CharField(max_length=256,null=True)
    # label = models.CharField(max_length=50,null=True)

    def __str__(self):
        return f'https://twitter.com/{self.username}'


class FetchedInterval(models.Model):
    id = models.AutoField(primary_key=True)
    twitter_user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)
    interval_start = models.DateField()
    complete = models.BooleanField(default=False)

    def __str__(self):
        return f'twitter_user:{self.twitter_user.username}, ' \
               f'interval start:{self.interval_start}, ' \
               f'complete:{self.complete}'


class Tweet(models.Model):
    id = models.AutoField(primary_key=True)
    twitter_user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE,related_name='twitter_user')
    twitter_id = models.BigIntegerField(unique=True)
    url = models.CharField(max_length=256)
    date = models.DateField()
    content = models.TextField()
    reply_count = models.IntegerField()
    retweet_count = models.IntegerField()
    like_count = models.IntegerField()
    quote_count = models.IntegerField()
    twitter_conversation_id = models.BigIntegerField()
    lang = models.CharField(max_length=50)
    sourceLabel = models.CharField(max_length=256,null=True)
    retweeted_tweet = models.ForeignKey('self', on_delete=models.SET_NULL,null=True,related_name='ref_to_retweeted_tweet')
    quoted_tweet = models.ForeignKey('self', on_delete=models.SET_NULL,null=True,related_name='ref_to_quoted_tweet')
    tweeter_in_reply_to_tweet_id = models.BigIntegerField(null=True)
    in_reply_to_user = models.ForeignKey(TwitterUser, on_delete=models.SET_NULL,related_name='in_reply_to_user',null=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    fetched_interval = models.ForeignKey(FetchedInterval, on_delete=models.CASCADE, related_name='fetched_interval')
    # place =

    def __str__(self):
        return self.url



