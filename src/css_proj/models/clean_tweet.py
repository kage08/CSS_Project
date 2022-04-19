import re


def process_text(tweet: str) -> str:
    """
    Process the text of the tweet.
    ---
    Parameters:
    ---
    tweet (str): The tweet text.
    """
    tweet = re.sub("((www\.[^\s]+)|(https?://[^\s]+))\s+", "", tweet)
    tweet = re.sub("\s+((www\.[^\s]+)|(https?://[^\s]+))", "", tweet)
    tweet = re.sub("((www\.[^\s]+)|(https?://[^\s]+))", " ", tweet)
    tweet = re.sub("^RT @[A-Za-z0-9_]+: ", "", tweet)
    tweet = re.sub(r"’", "'", tweet)
    user_str = "^[\s.]*@[A-Za-z0-9_]+\s+"
    change = re.sub(user_str, "", tweet)
    while change != tweet:
        tweet = change
        change = re.sub(user_str, "", tweet)
    tweet = change
    tweet = re.sub("[\s]+", " ", tweet)
    tweet = re.sub(r"#([^\s]+)", r"\1", tweet)
    tweet = re.sub(r" &amp; ", " and ", tweet)
    tweet = re.sub(r"&amp;", " and ", tweet)
    tweet = re.sub(r"[^\x00-\x7F]+", "", tweet)
    tweet = tweet.strip("'\"")
    tweet = tweet.lower().strip()
    return tweet
