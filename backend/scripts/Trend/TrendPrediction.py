import random
from datetime import datetime, timedelta
from itertools import chain

import numpy as np
import pytz
from django.db.models import Max
# from keras.models import Sequential, Model
# from keras.layers import Reshape, Input, Dense, Conv1D, MaxPooling1D, GlobalMaxPooling1D, TextVectorization, InputLayer, Concatenate, Embedding
# import tensorflow as tf

from scripts.Trend.config import LDA_SIZE, TRENDS_NUMBER, DAILY_MAX_TREND
from scripts.preprocess import tweet_preprocess, trend_preprocess
from tweet.models import Tweet, Trend, TrendOccurrence, TrendPredictionData
from twipper.config import OLDEST_TWEET_DATE, KERAS_SAVE_LOCATION


# def create_model():
#     max_length = 100000
#     max_words = 10000
#
#     text_input_layer = Input(shape=(1,))
#     text_input_layer = InputLayer(input_shape=(1,), dtype=tf.string)(text_input_layer)
#     text_input_layer = TextVectorization(max_tokens=max_words, output_sequence_length=max_length)(text_input_layer)
#     text_input_layer = Embedding(max_words, 256, input_length=max_length)(text_input_layer)
#     # text_input_layer = Conv1D(256, 7, activation='relu',name='conv1')(text_input_layer)
#     # text_input_layer = MaxPooling1D(5)(text_input_layer)
#
#     # trend_input_layer = Input(shape=(480*LDA_SIZE))
#     # trend_input_layer = Dense(480)(trend_input_layer)
#     # trend_input_layer = Dense(256)(trend_input_layer)
#     # trend_input_layer = Reshape((256,1))(trend_input_layer)
#     # trend_input_layer = Conv1D(256, 7, activation='relu')(trend_input_layer)
#     # trend_input_layer = MaxPooling1D(5)(trend_input_layer)
#     #
#     # output = Concatenate(axis=1)([text_input_layer, trend_input_layer])
#     # output = Conv1D(64, 7, activation='relu')(output)
#     output = Conv1D(256, 7, activation='relu',name='conv2')(text_input_layer)
#     output = MaxPooling1D(5)(output)
#     output = Conv1D(128, 7, activation='relu',name='conv3')(output)
#     output = GlobalMaxPooling1D()(output)
#     output = Dense(TRENDS_NUMBER*LDA_SIZE, activation='sigmoid')(output)
#     # model = Model([text_input_layer, trend_input_layer], output)
#     model = Model(text_input_layer, output)
#     model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
#
#     return model


def train():
    accepted_trends = Trend.objects.filter(topic__isnull=False).values_list('name',flat=True)
    TrendPredictionData.objects.all().delete()
    days = []
    day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    while day > OLDEST_TWEET_DATE - timedelta(days=1):
        days.append(day)
        day -= timedelta(days=1)
    x_text = []
    x_trend = []
    y = []
    random.shuffle(days)
    for day in days:
        text,trend,out = get_data_by_date(day,accepted_trends)
        if out is None:
            continue
        # break
        x_text.append(text)
        x_trend.append(trend)
        y.append(out)
        TrendPredictionData.objects.create(date = day.date(),text=text,topic=trend,target_topic=out)
    return
    # x_text = np.asarray(x_text).astype('str').reshape((len(days),1,))
    # x_trend = np.asarray(x_trend).astype('float32').reshape((len(days),480*LDA_SIZE,))
    # y = np.asarray(y).astype('float32').reshape((len(days),5*LDA_SIZE,))
    #
    # # x = np.empty(shape=(len(days),2))
    # # for i in range(len(days)):
    # #     x[i] = np.array([x_text[i],x_trend[i]])
    #
    # train_to_test_ratio = 3
    # divider = int((train_to_test_ratio*len(x_text))/(train_to_test_ratio+1))
    # train_x_text = x_text[:divider]
    # test_x_text = x_text[divider:]
    # train_x_trend = x_trend[:divider]
    # test_x_trend = x_trend[divider:]
    # train_y = y[:divider]
    # test_y = y[divider:]
    # train_x = x_text[:divider]
    # test_x = x_text[divider:]
    # model = create_model()
    # model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    #     filepath=KERAS_SAVE_LOCATION,
    #     save_weights_only=True,
    #     monitor='val_loss',
    #     mode='min',
    #     save_best_only=True)
    #
    # model.fit(
    #     x=train_x_text, y=train_y,
    #     validation_data=(test_x_text, test_y),
    #     epochs=200, batch_size=8,callbacks=[model_checkpoint_callback])
    # model.save(KERAS_SAVE_LOCATION)


def get_data_by_date(day:datetime,accepted_trends:list):
    texts = Tweet.objects.filter(date__gte=day.replace(tzinfo=pytz.UTC), date__lte=day.replace(tzinfo=pytz.UTC) + timedelta(days=1)).values_list('content', flat=True)
    text = ''
    for txt in texts:
        pre_txt = tweet_preprocess(txt)
        if pre_txt is not None:
            text += " " + pre_txt
    # print(text)
    trend = TrendOccurrence.objects.filter(date=day.replace(tzinfo=pytz.UTC).date()).values_list('trend__name',flat=True)
    trend = trend[:min([DAILY_MAX_TREND, len(trend)])]
    trend = [tre for tre in trend if tre in accepted_trends]
    if len(trend) < 10:
        return None,None,None
    # print(trend)
    out = TrendOccurrence.objects.filter(date=day.replace(tzinfo=pytz.UTC).date()+timedelta(days=1)
                                         ,tweet_count__isnull=False).values('trend__name'). \
        annotate(total_tweet=Max('tweet_count')).order_by('-total_tweet')
    out = [o['trend__name'] for o in out]
    out = out[:min([TRENDS_NUMBER,len(out)])]
    out = [o for o in out if o in accepted_trends]
    if len(out) == 0:
        return None,None,None
    return text,trend,out