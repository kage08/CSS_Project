import tweepy
from .consts import ACCESS_KEY, ACCESS_SECRET, API_KEY, API_SECRET


def initialize_api(
    consumer_key: str = API_KEY,
    consumer_secret: str = API_SECRET,
    access_token: str = ACCESS_KEY,
    access_token_secret: str = ACCESS_SECRET,
):
    """
    Initialize the tweepy API.

    ---
    Parameters:
    ---
    consumer_key (str): The consumer key.
    consumer_secret (str): The consumer secret.
    access_token (str): The access token.
    access_token_secret (str): The access token secret.
    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api
