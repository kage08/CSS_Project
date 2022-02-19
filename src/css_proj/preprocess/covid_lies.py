import os, requests
from .consts import COVID_LIES_PATH, COVID_LIES_URL

def download_covid_lies(url: str=COVID_LIES_URL, path: str=COVID_LIES_PATH):
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

