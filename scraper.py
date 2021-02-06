import requests
import lxml
import re
import random
from bs4 import BeautifulSoup

def get_soup(wikipage):
    """makes a BeautifulSoup object from a generic URL

    Args:
        wikipage (str): a URL for the webpage you want to soup-ify

    Returns:
        bs4.BeautifulSoup: A BeautifulSoup object which soup-ifies the given URL
    """
    page = requests.get(wikipage)
    page.raise_for_status()
    return BeautifulSoup(page.text, 'lxml')

    # get all 'a' tags on the page that have an 'href' atrribute
    new_pages = soup.select('a[href]')

    # Just in case there are no href's, search a random article instead
    while new_pages == []:
        # Erases the "page we came from" since we couldn't find any new wikipages there
        prev_page = None

        # Travel to a random wikipage
        soup = get_soup('https://en.wikipedia.org/wiki/Special:Random')
        # Try finding the new_pages from the new wikipage
        new_pages = soup.select('a[href]')

    # BUG: throws KeyError if there are no 'a' tags in the soup
    # This shouldn't be a problem though, since Wikipedia avoids dead pages like this? See: https://en.wikipedia.org/wiki/Category:Dead-end_pages
    # Just in case I'll just throw None if it happens
    try:
        new_pages = [page['href'] for page in soup.select('a[href]')]
    except:
        return None
    new_pages = set(wiki_page for wiki_page in new_pages if re.search(
        '^\/wiki\/(?!\w*:\w*).+$', wiki_page))    # only keep wiki_pages that look like '\wiki\<something>'
    # for page in new_pages:
    #     print(page)
    return  'https://en.wikipedia.org' + random.choice(tuple(new_pages))

print(get_page())