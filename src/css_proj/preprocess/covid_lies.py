import os, requests
import pandas as pd
from .consts import (
    COVID_LIES_PATH,
    COVID_LIES_URL,
)
import tweepy
from tqdm import tqdm
import logging
import pickle


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

INTERMEDIATE_PATH = "./data/data_processed/lies_data_intermediate.pkl"


def get_empty_df_lies(path: str = COVID_LIES_PATH, save: bool = True):
    """
    Get an empty dataset for the COVID-19 cure dataset.

    ---
    Parameters:
    ---
    path (str): The path to the COVID-19 lies dataset (csv).
    """
    if os.path.exists(INTERMEDIATE_PATH):
        df = load_intermediate_df_lies()
        return df

    df = pd.read_csv(path)
    df["state"] = 0
    df["tweet_text"] = ""
    df["retweets"] = 0
    df["likes"] = 0
    df["created"] = ""
    df["lang"] = ""
    df["device"] = ""
    df["user_id"] = 0
    df["user_name"] = ""
    df["user_handle"] = ""
    df["user_location"] = ""
    df["user_description"] = ""
    df["user_following"] = 0
    df["user_followers"] = 0
    df["user_verified"] = 0
    df["user_total_tweets"] = 0
    df["user_total_likes"] = 0
    df["user_total_lists"] = 0
    df["misconception_id"] = ""
    if save:
        save_intermediate_df_lies(df)
    return df


def save_intermediate_df_lies(df, path: str = INTERMEDIATE_PATH):
    """
    Save the intermediate dataset to the given path.

    ---
    Parameters:
    ---
    path (str): The path to the intermediate dataset.
    """
    with open(path, "wb") as f:
        pickle.dump(df, f)


def load_intermediate_df_lies(path: str = INTERMEDIATE_PATH):
    """
    Load the intermediate dataset from the given path.

    ---
    Parameters:
    ---
    path (str): The path to the intermediate dataset.
    """
    with open(path, "rb") as f:
        return pickle.load(f)


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


def get_tweet_info(df: pd.DataFrame, idx: int, api):
    """
    Get the tweet info of the tweet with the given index.

    ---
    Parameters:
    ---
    idx (int): The index of the tweet.
    """

    tweet_id = df.iloc[idx]["tweet_id"]
    if df.iloc[idx]["state"] != 0:
        return df
    try:
        feat_dict = get_tweet_features(tweet_id, api)
        for feat in feat_dict:
            df.iloc[idx, df.columns.get_loc(feat)] = feat_dict[feat]
        df.iloc[idx, df.columns.get_loc("state")] = 1
        save_intermediate_df_lies(df)
        return df
    except Exception as e:
        if "Forbidden" in str(e):
            df.iloc[idx, df.columns.get_loc("state")] = -1
            save_intermediate_df_lies(df)
            print(e)
            return df
        print(f"Failed to get tweet {tweet_id} at index {idx}")
        print(e)
        return e


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


def get_df_lies(
    api, path: str = COVID_LIES_PATH, start_idx: int = 0, end_idx: int = -1
):
    """
    Get the COVID-19 cure dataset from the given path.

    ---
    Parameters:
    ---
    path (str): The path to the COVID-19 lies dataset (csv).
    """
    df = get_empty_df_lies(path, save=True)
    if end_idx == -1:
        end_idx = len(df)
    for idx in tqdm(range(start_idx, end_idx)):
        df = get_tweet_info(df, idx, api)
        if type(df) != pd.DataFrame:
            print("Rate limit exceeded at index {}".format(idx))
            print("Try again later")
            break
    return df


def clean_up_intermediate(
    path: str = INTERMEDIATE_PATH,
    save_path="./data/data_processed/lies_data_cleaned.pkl",
):
    """
    Clean up the intermediate dataset.

    ---
    Parameters:
    ---
    path (str): The path to the intermediate dataset.
    """
    df = load_intermediate_df_lies(path)
    df = df[df["state"] == 1]
    df = df.drop(columns=["state"])
    with open(save_path, "wb") as f:
        pickle.dump(df, f)
    return df
