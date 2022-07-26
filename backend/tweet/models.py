from django.db import models


class TwitterUser(models.Model):
    username = models.CharField(max_length=16, unique=True)
    id = models.AutoField(primary_key=True)
    # twitter_id = models.IntegerField(unique=True)
    display_name = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)
    verified = models.BooleanField(null=True)
    created = models.DateField(null=True)
    followers_count = models.IntegerField(null=True)
    friends_count = models.IntegerField(null=True)
    statuses_count = models.IntegerField(null=True)
    favourites_count = models.IntegerField(null=True)
    location = models.CharField(max_length=50, null=True)
    protected = models.BooleanField(null=True)
    profile_image_url = models.CharField(max_length=255, null=True)
    profile_banner_url = models.CharField(max_length=255, null=True)

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


class Trend(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    topic = models.JSONField(null=True)

    def __str__(self):
        return self.name


class Tweet(models.Model):
    id = models.AutoField(primary_key=True)
    twitter_user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE, related_name='twitter_user')
    twitter_id = models.BigIntegerField(unique=True)
    url = models.CharField(max_length=255)
    date = models.DateTimeField()
    content = models.TextField()
    reply_count = models.IntegerField()
    retweet_count = models.IntegerField()
    like_count = models.IntegerField()
    quote_count = models.IntegerField()
    twitter_conversation_id = models.BigIntegerField()
    lang = models.CharField(max_length=50)
    sourceLabel = models.CharField(max_length=255, null=True)
    retweeted_tweet = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,
                                        related_name='ref_to_retweeted_tweet')
    quoted_tweet = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='ref_to_quoted_tweet')
    tweeter_in_reply_to_tweet_id = models.BigIntegerField(null=True)
    in_reply_to_user = models.ForeignKey(TwitterUser, on_delete=models.SET_NULL, related_name='in_reply_to_user',
                                         null=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    fetched_interval = models.ForeignKey(FetchedInterval, on_delete=models.CASCADE, related_name='fetched_interval',null=True)
    trend = models.ForeignKey(Trend, on_delete=models.CASCADE, related_name='trend',null=True)

    # place =

    def __str__(self):
        return self.url


class Collection(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, default='done')

    def __str__(self):
        return self.name


class CollectionTwitterUser(models.Model):
    id = models.AutoField(primary_key=True)
    twitter_user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class Place(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return self.name


class TrendOccurrence(models.Model):
    id = models.AutoField(primary_key=True)
    trend = models.ForeignKey(Trend, on_delete=models.CASCADE, null=False)
    date = models.DateField(null=False)
    time = models.TimeField(null=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=False)
    tweet_count = models.IntegerField(null=True)
    # top = models.BooleanField(default=False)

    def __str__(self):
        return self.trend.name + ":" + str(self.date)


class TrendPredictionData(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(null=False)
    text = models.TextField(null=False)
    topic = models.JSONField(null=False)
    target_topic = models.JSONField(null=False)

    def __str__(self):
        return self.date


class LDATopic(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(null=False, max_length=2, unique=True)
    words = models.CharField(null=False, max_length=255)

    def __str__(self):
        return self.name


class UserTopic(models.Model):
    id = models.AutoField(primary_key=True)
    week_number = models.IntegerField()
    topic = models.ForeignKey(LDATopic, on_delete=models.CASCADE, null=False)
    twitter_user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)
    value = models.FloatField(null=False, default=0)

    def __str__(self):
        return self.topic.name+ ':' + str(self.value)


class UserTopicARIMA(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(LDATopic, on_delete=models.CASCADE, null=False)
    twitter_user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)
    value = models.CharField(max_length=255,null=False, default='')
    train_loss = models.FloatField(null=False, default=0)
    val_loss = models.FloatField(null=False, default=0)

    def __str__(self):
        return self.topic.name+ ':' + self.value
    
    
class Trend_TABLEDATA(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=16)
    text = models.TextField()
    date = models.DateTimeField()
    trend = models.CharField(max_length=255)
    # topic = models.ForeignKey(LDATopic, on_delete=models.CASCADE, null=False)
    # twitter_user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)
    # value = models.CharField(max_length=255,null=False, default='')
    # train_loss = models.FloatField(null=False, default=0)
    # val_loss = models.FloatField(null=False, default=0)

    def __str__(self):
        return self.topic.name+ ':' + self.value