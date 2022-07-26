from django.urls import path

from . import views
from .views import CollectionApiView, CollectionIdApiView, TwitterUserIdApiView

urlpatterns = [
    path('', views.index, name='index'),


    # collection
    path('collection/api/', CollectionApiView.as_view()),
    path('collection/api/<int:collection_id>/', CollectionIdApiView.as_view()),


    # twitter_user
    path('twitteruser/api/<str:twitter_user_username>/', TwitterUserIdApiView.as_view()),


    # custom api

    # user analysis page api
    path('get_users_by_collection/<int:collection_id>/', views.get_users_by_collection, name='get_users_by_collection'),
    path('get_user_info_by_id/<int:user_id>/', views.get_user_info_by_id, name='get_user_info_by_id'),
    path('get_user_tweet_count_chart1_by_id/<int:user_id>/<int:interval>/', views.get_user_tweet_count_chart1_by_id, name='get_user_tweet_count_chart1_by_id'),
    path('get_user_tweet_count_chart2_by_id/<int:user_id>/<int:interval>/', views.get_user_tweet_count_chart2_by_id, name='get_user_tweet_count_chart2_by_id'),
    path('get_user_TF_chart1_by_id/<int:user_id>/<str:start_date>/<str:stop_date>/', views.get_user_TF_chart1_by_id, name='get_user_TF_chart1_by_id'),
    path('get_user_LDA_chart1_by_id/<int:user_id>/<int:interval>/', views.get_user_LDA_chart1_by_id, name='get_user_LDA_chart1_by_id'),
    path('get_user_LDA_chart2_by_id/<int:user_id>/<int:interval>/', views.get_user_LDA_chart2_by_id,name='get_user_LDA_chart2_by_id'),
    path('get_user_ARIMA_chart_by_id/<int:user_id>/<int:interval>/', views.get_user_ARIMA_chart_by_id,name='get_user_ARIMA_chart_by_id'),
    path('get_collection_ARIMA_chart/<int:collection_id>/', views.get_collection_ARIMA_chart,name='get_collection_ARIMA_chart'),
    path('get_table_correlation/<int:collection_id>/', views.get_table_correlation,name='get_table_correlation'),

    path('scripts/', views.scripts, name='scripts'),
]