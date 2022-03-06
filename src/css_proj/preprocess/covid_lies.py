import os, requests
import pandas as pd
from .consts import (
    COVID_LIES_PATH,
    COVID_LIES_URL,
    API_KEY,
    API_SECRET,
    ACCESS_KEY,
    ACCESS_SECRET,
)
import tweepy
from tqdm import tqdm
import logging



cvl_features = [
    "tweet_id",
    "tweet_text",
    "retweets",
    "likes",
    "created",
    "lang",
    "device",
    "user_id",
    "user_name",
    "user_handle",
    "user_location",
    "user_description",
    "user_following",
    "user_followers",
    "user_verified",
    "user_total_tweets",
    "user_total_likes",
    "user_total_lists",
    "misconception_id",
    "label",
]


def download_covid_lies(url: str = COVID_LIES_URL, path: str = COVID_LIES_PATH):
    """
    Download the COVID-19 lies dataset from the given URL and save it to the given path.

    ---
    Parameters:
    ---
    url (str): The URL of the COVID-19 lies dataset.
    path (str): The path to save the COVID-19 lies dataset.
    """
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    print("Downloading covid_lies.csv from github...")
    r = requests.get(url)
    with open(path, "wb") as f:
        f.write(r.content)
    print("Done.")


def get_tweet_features(tweet_id: str, api) -> dict:
    """
    Get the features of the tweet with the given tweet_id.

    ---
    Parameters:
    ---
    tweet_id (str): The tweet_id of the tweet.
    """
    entry = dict()
    entry["tweet_id"] = tweet_id
    tweet = api.get_status(tweet_id)
    entry["tweet_text"] = tweet.text
    entry["retweets"] = tweet.retweet_count
    entry["likes"] = tweet.favorite_count
    entry["created"] = tweet.created_at
    entry["lang"] = tweet.lang
    entry["device"] = tweet.source
    user = tweet.user
    entry["user_id"] = user.id
    entry["user_name"] = user.name
    entry["user_handle"] = user.screen_name
    entry["user_location"] = user.location
    entry["user_description"] = user.description
    entry["user_following"] = user.friends_count
    entry["user_followers"] = user.followers_count
    entry["user_verified"] = user.verified
    entry["user_total_tweets"] = user.statuses_count
    entry["user_total_likes"] = user.favourites_count
    entry["user_total_lists"] = user.listed_count
    return entry


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


def get_df_covid_lies(api, path: str = COVID_LIES_PATH, start_idx: int = 0):
    """
    Get the COVID-19 lies dataset from the given path.

    ---
    Parameters:
    ---
    path (str): The path to the COVID-19 lies dataset (csv).
    """
    dataset = pd.DataFrame(columns=cvl_features)
    df = pd.read_csv(path)
    # Log to file
    logging.basicConfig(filename="logs/covid_lies_extract.log", level=logging.INFO)

    for i in tqdm(range(start_idx, len(df))):
        try:
            entry = get_tweet_features(str(df.iloc[i]["tweet_id"]), api)
            entry["misconception_id"] = df.iloc[i]["misconception_id"]
            entry["label"] = df.iloc[i]["label"]
            dataset = pd.concat([dataset, pd.DataFrame([entry])], ignore_index=True)
            logging.info(f"Extracted tweet {df.iloc[i]['tweet_id']}")
        except Exception as e:
            logging.warning(f"Failed to get tweet {df.iloc[i]['tweet_id']}")
            logging.warning(e)
            continue
    return dataset
