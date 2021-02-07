
import scraper
import textwrap
import re
import logging
import logging.handlers

logger = logging.getLogger(__name__)
# set log level
logger.setLevel(logging.INFO)

# define file handler and set formatter
file_handler = logging.handlers.RotatingFileHandler('log/tweet.log', maxBytes = 50000, backupCount=1)
formatter = logging.Formatter(
    '%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)

# add file handler to logger
logger.addHandler(file_handler)


def compose_tweet(page):
    """Composes a tweet that's ready to be posted in this format

    <NEW TITLE>

    From here: <URL>
    I got to here: <NEW URL>

    Args:
        URL (string): A URL containing a wikipage whose links we need to search
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


def tweet(URL):
    """does the actual tweeting

    Args:
        URL (string): A URL containing a wikipage whose links we need to search
    """
    # make the actual message to tweet out

    # update prev_page.txt

    # tweet it out


logger.info("Started tweet.py driver code")
for _ in range(5):
    with open('prev_page.txt', 'r') as prevf:
        prev_page = prevf.read()
    print(compose_tweet(prev_page))
# with open('prev_page.txt', 'r') as prevf:
#     prev_page = prevf.read()
# print(compose_tweet(prev_page))
logger.info("Finished tweet.py driver code")
