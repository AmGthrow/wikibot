import requests
import lxml
import re
import random
import logging
import logging.handlers
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)
# set log level
logger.setLevel(logging.INFO)

# define file handler and set formatter
file_handler = logging.handlers.RotatingFileHandler('wikibot.log', maxBytes = 50000)
formatter = logging.Formatter(
    '%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)

# add file handler to logger
logger.addHandler(file_handler)


class Wikipage:
    def __init__(self, url):
        self.url = url
        self.soup = self.get_soup(self.url)
        self.title = self.get_title()

    def get_soup(self, wikipage):
        """makes a BeautifulSoup object from a generic URL

        Args:
            wikipage (str): a URL for the webpage you want to soup-ify

        Returns:
            bs4.BeautifulSoup: A BeautifulSoup object which soup-ifies the given URL
        """
        page = requests.get(wikipage)
        page.raise_for_status()
        return BeautifulSoup(page.text, 'lxml')

    def get_page(self):
        """Returns a URL to another wikipage using a link that exists in a given wikipage

        Returns:
            prev_page: a URL to a Wikipedia page with a backlink to self.url
        """

        # soup-ify the wikipage URL
        soup = self.soup

        # get all 'a' tags on the page that have an 'href' atrribute
        new_pages = soup.select('p > a[href]')

        # Just in case there are no href's, search a random article instead
        while new_pages == []:
            # Travel to a random wikipage
            soup = self.get_soup(
                'https://en.wikipedia.org/wiki/Special:Random')
            # Try finding the new_pages from the new wikipage instead
            new_pages = soup.select('p > a[href]')

        # extract only the 'href' attribute in all the tags
        new_pages = [page['href'] for page in new_pages]
        # Turn new_pages into a set to remove dupliactes
        new_pages = set(wiki_page for wiki_page in new_pages if re.search(
            '^\/wiki\/(?!\w*:\w*).+$', wiki_page))    # only keep wiki_pages that look like '\wiki\<something>'

        #  manually remove '/wiki/Main_Page'. It looks remarkably like a regular wikipage but it's the only one that's this similar
        if '/wiki/Main_Page' in new_pages:
            new_pages.remove('/wiki/Main_Page')

        for page in new_pages:    # TODO: Use a logger instead of a print
            logger.info(f"Found page: {page}")

        # Concatenate the wikipedia domain with a random href
        new_page = 'https://en.wikipedia.org' + random.choice(tuple(new_pages))
        # Make sure we don't just link to the current page
        while new_page == self.url:
            new_page = 'https://en.wikipedia.org' + \
                random.choice(tuple(new_pages))
        logger.info(f'selected {new_page}')
        return new_page

    def get_title(self):
        return self.soup.select_one('#firstHeading').text

    def summarize(self):
        # I don't always need to summarize, so writing it this way ensures that
        # 1) I only call select_one() once
        # 2) I never actually call select_one() unless I have to (i.e. self.summary doesn't exist until I call summarize())
        # This means I don't waste resources trying to summarize webpages that I don't even need the summary for
        if not hasattr(self, 'summary'):
            self.summary = self.soup.select_one(
                '.mw-parser-output p:not([class])').text
        return self.summary


if __name__ == "__main__":
    page = Wikipage('https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon')
    print(page.url)
    print(page.get_page())
    print(page.get_title())
    print(page.summarize())
    print(page.summary)
