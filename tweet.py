
import scraper
import textwrap
import re
import logging
import logging.handlers
import tweepy
from os import getenv

# These are Twitter constants that I rely on for when I'm making a tweetable message, mostly for shorten_summary()
MAX_TWEET_LENGTH = 280
URL_LENGTH = 23  # All URLs have a fixed length, see number 2 in https://help.twitter.com/en/using-twitter/how-to-tweet-a-link

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


def compose_tweet(page, fit_tweet_limit=False, erase_prev=True):
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

    # fit_tweet_limit means you want to keep the message under MAX_TWEET_LENGTH to fit the Twitter character limit
    if fit_tweet_limit:
        new_summary = shorten_summary(new_title, new_summary)

    message = f"""\
    {new_title}

    From here: {prev_url}
    I got to here: {new_url}

    {new_summary}"""

    # log the composed message
    logger.info(f"composed message:\n\n{message}")

    if erase_prev:
        # Overwrite whatever was in prev_page.txt
        with open('prev_page.txt', 'w') as prevf:
            prevf.write(new_url)

    return textwrap.dedent(message)


def shorten_summary(title, summary):
    """Receives a potential tweet which may be longer than MAX_TWEET_LENGTH. If so, it cuts off the summary and adds an ellipsis

    Args:
        title (str): The title of the potential tweet
        summary (str): The summary 

    Returns:
        str: The same summary except cut down to fit MAX_TWEET_LENGTH, ending in '...' if it was trimmed
    """
    # chars_remaining tracks how long my summary is allowed to be
    chars_remaining = MAX_TWEET_LENGTH
    chars_remaining -= len(title)   # Subtracts the title
    # Subtracts the two "transformed URL lengths" of prev_page and new_page
    chars_remaining -= URL_LENGTH * 2
    # This is just the length of the "from here I got to here" part, including newlines and spaces
    chars_remaining -= 29
    # BUG: I have NO idea why but this function just CONSISTENTLY has 2 excess characters so I guess I have to shave those off
    chars_remaining -= 2

    # Trim off whatever excess remains since at this point, they have no chance of being included anyway
    summary = summary[:chars_remaining - 3]  # -3 to make room for ellipsis
    summary += '...'

    # There are some Unicode characters that Twitter gives a weight of 2, not just 1. e.g. Emojis should reduce chars_remaining by 2, not just 1
    # See this: https://developer.twitter.com/en/docs/counting-characters
    # So I need to keep track of those letters and subtract the 'extra weight' from chars_remaining. This for loop does exactly that

    # If I find any 2-weight characters in summary, deduct chars_remaining accordingly
    for s in summary:
        code_point = ord(s)
        if not (0 <= code_point <= 4351 or
                8192 <= code_point <= 8205 or
                8208 <= code_point <= 8223 or
                8242 <= code_point <= 8247):
            # subtract 1 instead of 2 since len(summary) already covers regular chars. I just need to reduce chars_remaining for ever 2-weight char I have
            chars_remaining -= 1

    # If summary is too long to fit into 1 tweet, cut it off and add an ellipsis
    if len(summary) > chars_remaining:
        # -3 to make room for the ellipsis
        summary = summary[:chars_remaining - 3]
        summary += '...'

    return summary


def tweet(url):
    """Connects to the Twitter API and sends out a tweet using compose_tweet(url)

    Args:
        url (str): The Wikipedia page whose links need to be searched
    """
    # make the actual message to tweet out
    message = compose_tweet(url, fit_tweet_limit=True)

    # tweet it out
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    api.update_status(message)


if __name__ == "__main__":
    logger.info('Started tweet.py driver code')
    with open('prev_page.txt', 'r') as prevf:
        prev_page = prevf.read()
    tweet(prev_page)
    logger.info("Finished tweet.py driver code")
