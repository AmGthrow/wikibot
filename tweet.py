
import scraper
import textwrap
import re


def compose_tweet(page):
    """Composes a tweet that's ready to be posted in this format

    <NEW TITLE>

    From here: <URL>
    I got to here: <NEW URL>

    Args:
        URL (string): A URL containing a wikipage whose links we need to search
    """
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


for _ in range(5):
    with open('prev_page.txt', 'r') as prevf:
        prev_page = prevf.read()
    print(compose_tweet(prev_page))
