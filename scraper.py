import requests
import lxml
import re
import random
from bs4 import BeautifulSoup


def get_page(wikipage='https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon'):
    page = requests.get(wikipage)
    page.raise_for_status()
    soup = BeautifulSoup(page.text, 'lxml')

    # get all 'a' tags on the page

    # BUG: throws KeyError if there are no 'a' tags in the soup
    # This shouldn't be a problem though, since Wikipedia avoids dead pages like this? See: https://en.wikipedia.org/wiki/Category:Dead-end_pages
    new_pages = set(wiki_page for wiki_page in new_pages if re.search(
        '^\/wiki\/(?!\w*:\w*).+$', wiki_page))    # only keep wiki_pages that look like '\wiki\<something>'
    # for page in new_pages:
    #     print(page)
    return  'https://en.wikipedia.org' + random.choice(tuple(new_pages))

print(get_page())