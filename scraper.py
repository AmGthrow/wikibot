import requests
import lxml
import re
import random
from bs4 import BeautifulSoup


def get_page(wikipage='https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon'):
    page = requests.get(wikipage)
    page.raise_for_status()
    soup = BeautifulSoup(page.text, 'lxml')

    # get all 'a' tags that appear inside a 'p' tag (there are lots of 'a' tags like navbars that I don't care about,
    # but the ones that are actually part of the page's "content" usually apear inside 'p' tags)
    # BUG: throws KeyError if there are no 'p a' tags in the soup
    new_pages = [page['href'] for page in soup.select('a[href]')]
    new_pages = set(wiki_page for wiki_page in new_pages if re.search(
        '^\/wiki\/(?!\w*:\w*).+$', wiki_page))    # only keep wiki_pages that look like '\wiki\<something>'
    # for page in new_pages:
    #     print(page)
    return random.choice(tuple(new_pages))

print(get_page())