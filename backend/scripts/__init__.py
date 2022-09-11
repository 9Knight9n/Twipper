from tweet.models import Collection

try:
    collections = Collection.objects.update(status='done')
except:
    print('no collection table.')