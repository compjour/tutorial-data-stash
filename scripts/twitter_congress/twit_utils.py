# Some general Twitter accessing utils
import tweepy
from math import ceil
TWITTER_PROFILE_BATCH_SIZE = 100

def get_api(creds):
    """
    Takes care of the Twitter OAuth authentication process and
    creates an API-handler to execute commands on Twitter

    Arguments:
      - creds (dict): {
            "consumer_secret": "xyz",
            "access_token": "abc",
            "access_token_secret": "def",
            "consumer_key": "jk"
        }

    Returns:
      A tweepy.api.API object

    """
    # Get authentication token
    auth = tweepy.OAuthHandler(consumer_key = creds['consumer_key'],
                               consumer_secret = creds['consumer_secret'])
    auth.set_access_token(creds['access_token'], creds['access_token_secret'])
    # create an API handler
    return tweepy.API(auth)



def get_profiles_from_ids(api, screen_names = [], user_ids = []):
    """
    `api` is a tweepy.API handle
    `user_ids` is a list of user ids
    `screen_names` is a list of screen names

    Either screen_names or user_ids is used, not both

    Returns: a list of dicts representing Twitter profiles
    """

    if screen_names:
        data = screen_names
        darg = 'screen_names'
    else:
        data = user_ids
        darg = 'user_ids'

    TWITTER_PROFILE_BATCH_SIZE = 100
    profiles = []
    for i in range(ceil(len(data) / TWITTER_PROFILE_BATCH_SIZE)):
        s = i * TWITTER_PROFILE_BATCH_SIZE
        uids = data[s:(s + TWITTER_PROFILE_BATCH_SIZE)]
        _args = {darg: uids}
        for user in api.lookup_users(**_args):
            profiles.append(user._json)

    return profiles
