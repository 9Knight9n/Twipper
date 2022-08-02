from datetime import datetime,timedelta

from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from scripts.User import get_user_by_username
from scripts.Tweet import get_user_tweets, save_collection_tweets
from tweet.models import TwitterUser, Collection, CollectionTwitterUser, FetchedInterval
from twipper.config import OLDEST_TWEET_DATE, FETCH_INTERVAL_DURATION


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class CollectionApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        collections = Collection.objects.all().values('name','id')
        return Response(collections, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        collection = Collection.objects.create(name=request.data.get('name'))
        collection_twitter_user = []
        for twitter_user in request.data.get('twitter_usernames'):
            twitter_user_obj = TwitterUser.objects.get(username=twitter_user)
            collection_twitter_user.append(CollectionTwitterUser(twitter_user=twitter_user_obj,collection=collection))
        CollectionTwitterUser.objects.bulk_create(collection_twitter_user)

        save_collection_tweets.after_response(collection)

        return Response({'id':collection.id}, status=status.HTTP_201_CREATED)


class CollectionIdApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # def get_object(self, todo_id, user_id):
    #     '''
    #     Helper method to get the object with given todo_id, and user_id
    #     '''
    #     try:
    #         return Todo.objects.get(id=todo_id, user = user_id)
    #     except Todo.DoesNotExist:
    #         return None

    # 3. Retrieve
    def get(self, request, collection_id, *args, **kwargs):
        max_interval = int((datetime.now() - OLDEST_TWEET_DATE).days)//int(FETCH_INTERVAL_DURATION.days)
        collection = Collection.objects.get(id=collection_id)
        # if collection.status != 'in progress':
        #     save_collection_tweets.after_response(collection)
        collection_twitter_user = CollectionTwitterUser.objects.filter(collection=collection).values('twitter_user__username','twitter_user__id')
        twitter_user_percentage = []
        for user in collection_twitter_user:
            intervals = FetchedInterval.objects.filter(twitter_user_id=user['twitter_user__id']).count()
            twitter_user_percentage.append({
                'name':user['twitter_user__username'],
                'progress':min([100,int((intervals/max_interval)*100)])
            })
        data = {
            'name':collection.name,
            'twitter_user_percentage':twitter_user_percentage,
            'done':all([item['progress'] == 100 for item in twitter_user_percentage])
        }
        return Response(data, status=status.HTTP_200_OK)

    # # 4. Update
    # def put(self, request, todo_id, *args, **kwargs):
    #     '''
    #     Updates the todo item with given todo_id if exists
    #     '''
    #     todo_instance = self.get_object(todo_id, request.user.id)
    #     if not todo_instance:
    #         return Response(
    #             {"res": "Object with todo id does not exists"},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     data = {
    #         'task': request.data.get('task'),
    #         'completed': request.data.get('completed'),
    #         'user': request.user.id
    #     }
    #     serializer = TodoSerializer(instance = todo_instance, data=data, partial = True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # # 5. Delete
    # def delete(self, request, todo_id, *args, **kwargs):
    #     '''
    #     Deletes the todo item with given todo_id if exists
    #     '''
    #     todo_instance = self.get_object(todo_id, request.user.id)
    #     if not todo_instance:
    #         return Response(
    #             {"res": "Object with todo id does not exists"},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     todo_instance.delete()
    #     return Response(
    #         {"res": "Object deleted!"},
    #         status=status.HTTP_200_OK
    #     )


class TwitterUserIdApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, twitter_user_username, *args, **kwargs):
        user_obj = get_user_by_username(twitter_user_username)
        if not isinstance(user_obj, str):
            return Response('valid username', status=status.HTTP_200_OK)
        else:
            return Response('invalid username', status=status.HTTP_204_NO_CONTENT)


def get_users_by_collection(request, collection_id):
    collection = Collection.objects.get(id=collection_id)
    collection_twitter_user = CollectionTwitterUser.objects.filter(collection=collection).values('twitter_user__display_name','twitter_user__username','twitter_user__id','twitter_user__profile_image_url')
    twitter_user_list = []
    for user in collection_twitter_user:
        twitter_user_list.append({
            'id': user['twitter_user__id'],
            'username': user['twitter_user__username'],
            'display_name': user['twitter_user__display_name'] if user['twitter_user__display_name'] is not None
                                                                else user['twitter_user__username'],
            'avatar':user['twitter_user__profile_image_url']
        })
    data = {'name': collection.name,'twitter_user_list': twitter_user_list}
    return JsonResponse(data, status=status.HTTP_200_OK)



def scripts(request):
    user = get_user_by_username('thekarami')
    result = get_user_tweets(user)
    for item in result:
        print(item)
    return HttpResponse(f"done extracting {result.count()} tweets.")