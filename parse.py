import requests
from bs4 import BeautifulSoup

url = 'http://gwent-cards.com/'
response = requests.get(url)
