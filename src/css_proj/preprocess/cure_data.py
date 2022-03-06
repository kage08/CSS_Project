import os, requests
import pandas as pd
from .consts import CURE_DATA_PATH
import tweepy
from tqdm import tqdm
import logging


cure_features = [
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
    "label",
]


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


def get_df_cure(api, path: str = CURE_DATA_PATH, start_idx: int = 0):
    """
    Get the COVID-19 cure dataset from the given path.

    ---
    Parameters:
    ---
    path (str): The path to the COVID-19 lies dataset (csv).
    """
    dataset = pd.DataFrame(columns=cure_features)
    df = pd.read_csv(path)
    # Log to file
    logging.basicConfig(filename="logs/covid_cure_extract.log", level=logging.INFO)

    for i in tqdm(range(start_idx, len(df))):
        try:
            entry = get_tweet_features(str(df.iloc[i]["tweet_id"]), api)
            entry["label"] = df.iloc[i]["label"]
            dataset = pd.concat([dataset, pd.DataFrame([entry])], ignore_index=True)
            logging.info(f"Extracted tweet {df.iloc[i]['tweet_id']}")
        except Exception as e:
            logging.warning(f"Failed to get tweet {df.iloc[i]['tweet_id']}")
            logging.warning(e)
            continue
    return dataset
