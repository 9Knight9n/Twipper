from tweet.models import Collection

collections = Collection.objects.update(status='done')