from datetime import datetime, timedelta
import os
import requests
from .consts import COVAXXY_PATH, COVAXXY_URL

# Getting covaxxy tweet-ids
def get_path_covaxxy(date: datetime) -> str:
    """
    Get the path to the covaxxy dataset for the given date.

    ---
    Parameters:
    ---
    date (datetime): The date for which to get the path.
    """
    dt = date.strftime("%Y-%m-%d")
    site = f"{COVAXXY_URL}files/tweet_ids--{dt}.txt"
    return site


def download_covaxxy(date: datetime, dest: str = COVAXXY_PATH):
    """
    Download the covaxxy dataset for the given date.

    ---
    Parameters:
    ---
    date (datetime): The date for which to download the dataset.
    dest (str): The path to save the dataset.
    """
    if not os.path.isdir(dest):
        os.makedirs(dest, exist_ok=True)
    site = get_path_covaxxy(date)
    filename = os.path.join(dest, date.strftime("%Y-%m-%d")) + ".txt"
    if os.path.isfile(filename):
        print(f"File already available at {filename}")
        return
    print(f"Downloading from {site} to {filename}")
    try:
        r = requests.get(site, allow_redirects=True)
        with open(filename, "wb") as fl:
            fl.write(r.content)
        print("Downloading done")
    except:
        print("Download error")


# Get from range of dates
def get_covaxxy_range(
    start_date: datetime, end_date: datetime, dest: str = COVAXXY_PATH
):
    """
    Get the covaxxy dataset for the given date range.

    ---
    Parameters:
    ---
    start_date (datetime): The start date for the range.
    end_date (datetime): The end date for the range.
    """
    for days in range((end_date - start_date).days):
        dt = start_date + timedelta(days=days)
        download_covaxxy(dt, dest)
