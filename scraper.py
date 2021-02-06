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


def get_page(wikipage='https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon'):
    """Returns a URL to another wikipage using a link that exists in a given wikipage

    Args:
        wikipage (str, optional): wikipedia page that potentially contains links to more wikipedia pages. 
            Defaults to 'https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon'.

    Returns:
        str: a URL to a randomly chosen wikipedia page
    """

    # soup-ify the wikipage URL
    soup = get_soup(wikipage)
    # Records the page that new_page came from
    prev_page = wikipage

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

    # Turn new_pages into a set to remove dupliactes
    new_pages = set(wiki_page for wiki_page in new_pages if re.search(
        '^\/wiki\/(?!\w*:\w*).+$', wiki_page))    # only keep wiki_pages that look like '\wiki\<something>'
    # for page in new_pages:
    #     print(page)

    # Concatenate the wikipedia domain with a random href
    new_page = 'https://en.wikipedia.org' + random.choice(tuple(new_pages))
    return new_page

print(get_page())