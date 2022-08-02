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
    path('get_users_by_collection/<int:collection_id>/', views.get_users_by_collection, name='get_users_by_collection'),


    path('scripts/', views.scripts, name='scripts'),
]