import requests
from bs4 import BeautifulSoup

url = 'http://gwent-cards.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
rows = soup.find_all('tr')[1:]
for row in rows:
    cols = row.find_all('td')[1:]  # except first entry which is for image
    cols = [ele.text.strip() for ele in cols]
    print(cols)
