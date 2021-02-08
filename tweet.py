
import scraper
import textwrap
import re
import logging
import logging.handlers
import tweepy
from os import getenv

logger = logging.getLogger(__name__)
# set log level
logger.setLevel(logging.INFO)

# define file handler and set formatter
file_handler = logging.handlers.RotatingFileHandler(
    'log/tweet.log', maxBytes=50000, backupCount=1)
formatter = logging.Formatter(
    '%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)

# add file handler to logger
logger.addHandler(file_handler)

# Get API keys and stuff
consumer_key = getenv("CONSUMER_KEY")
consumer_secret = getenv("CONSUMER_SECRET")
access_token = getenv("ACCESS_TOKEN")
access_token_secret = getenv("ACCESS_TOKEN_SECRET")


def compose_tweet(page):
    """Composes a tweet that's ready to be posted in this format

    <NEW TITLE>

    From here: <URL>
    I got to here: <NEW URL>

    <SUMMARY OF NEW PAGE>
    """
    logger.info(f"Composing tweet for {page}")
    # Make Wikipage objects representing the current page
    prev_page = scraper.Wikipage(page)

    # get a new page from the current page
    new_page = scraper.Wikipage(prev_page.get_page())

    # return a composed message
    new_title = new_page.get_title().upper()
    prev_url = prev_page.url
    new_url = new_page.url
    new_summary = new_page.summarize()

    # Get rid of Wikipedia citations (they look like this[1]) from the summary
    new_summary = re.sub(r'\[\d+\]', '', new_summary)

    message = f"""
    {new_title}

    From here: {prev_url}
    I got to here: {new_url}

    {new_summary}
    """

    # Overwrite whatever was in prev_page.txt
    with open('prev_page.txt', 'w') as prevf:
        prevf.write(new_url)

    return textwrap.dedent(message)


def tweet():
    """does the actual tweeting

    Args:
        URL (string): A URL containing a wikipage whose links we need to search
    """
    # make the actual message to tweet out
    with open('prev_page.txt', 'r') as prevf:
        prev_page = prevf.read()
    message = compose_tweet(prev_page)

    # Make sure message fits the 280 character limit (with room for an ellipsis)
    message = message[:277] + '...'

    # tweet it out
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    api.update_status(message)


# logger.info("Started tweet.py driver code")
# for _ in range(5):
#     with open('prev_page.txt', 'r') as prevf:
#         prev_page = prevf.read()
#     print(compose_tweet(prev_page))
# # with open('prev_page.txt', 'r') as prevf:
# #     prev_page = prevf.read()
# # print(compose_tweet(prev_page))
# logger.info("Finished tweet.py driver code")

if __name__ == "__main__":
    tweet()
