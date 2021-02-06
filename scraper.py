from bs4 import BeautifulSoup
import requests
import lxml
import re

page = requests.get('https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon')
page.raise_for_status()
soup = BeautifulSoup(page.text, 'lxml')

new_pages = [page['href'] for page in soup.select('p a')]
print(new_pages)
