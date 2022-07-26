from django.urls import path

from . import views
from .views import CollectionApiView, CollectionIdApiView, TwitterUserIdApiView

urlpatterns = [
    path('', views.index, name='index'),


    # collection
    path('collection/api/', CollectionApiView.as_view()),
    path('collection/api/<str:collection_name>/', CollectionIdApiView.as_view()),


    # twitter_user
    path('twitteruser/api/<str:twitter_user_username>/', TwitterUserIdApiView.as_view()),


    path('scripts/', views.scripts, name='scripts'),
]