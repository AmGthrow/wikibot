import requests
import lxml
import re
import random
from bs4 import BeautifulSoup


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
        new_pages = soup.select('a[href]')

        # Just in case there are no href's, search a random article instead
        while new_pages == []:
            # Travel to a random wikipage
            soup = self.get_soup(
                'https://en.wikipedia.org/wiki/Special:Random')
            # Try finding the new_pages from the new wikipage instead
            new_pages = soup.select('a[href]')

        # extract only the 'href' attribute in all the tags
        new_pages = [page['href'] for page in new_pages]
        # Turn new_pages into a set to remove dupliactes
        new_pages = set(wiki_page for wiki_page in new_pages if re.search(
            '^\/wiki\/(?!\w*:\w*).+$', wiki_page))    # only keep wiki_pages that look like '\wiki\<something>'
        # for page in new_pages:    # TODO: Use a logger instead of a print
        #     print(page)

        # Concatenate the wikipedia domain with a random href
        new_page = 'https://en.wikipedia.org' + random.choice(tuple(new_pages))
        # Make sure we don't just link to the current page
        while new_page == self.url:
            new_page = 'https://en.wikipedia.org' + random.choice(tuple(new_pages))

        return new_page

    def get_title(self):
        return self.soup.select_one('#firstHeading').text


if __name__ == "__main__":
    page = Wikipage('https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon')
    print(page.url)
    print(page.get_page())
    print(page.get_title())
