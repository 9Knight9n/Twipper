import snscrape.modules.twitter as sntwitter

from tweet.models import TwitterUser


def extract_user_by_username(username:str):
    profile = sntwitter.TwitterUserScraper(username)._get_entity()
    obj = TwitterUser.objects.create(
        username = profile.username,
        # twitter_id = profile.id,
        display_name = profile.displayname,
        description = profile.rawDescription,
        verified = profile.verified,
        created = profile.created,
        followers_count = profile.followersCount,
        friends_count = profile.friendsCount,
        statuses_count = profile.statusesCount,
        favourites_count = profile.favouritesCount,
        location = profile.location,
        protected = profile.protected,
        profile_image_url = profile.profileImageUrl,
        profile_banner_url = profile.profileBannerUrl,
        # label = profile.label
    )
    return obj


def get_user_by_username(username:str):
    user = TwitterUser.objects.filter(username=username)
    if user.count() > 0:
        return user[0]
    try:
        user = extract_user_by_username(username)
        return user
    except AttributeError:
        return 'User is probably private. or something else :/'
    except Exception as e:
        return e.__str__()

# def search_user_by_possible_username(possible_username:str):
#     for result in sntwitter.TwitterSearchScraper(f'{possible_username}').get_items():
#         print('inside')
#         print(result)
#         break