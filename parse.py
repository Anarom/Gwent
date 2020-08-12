import requests
from bs4 import BeautifulSoup


def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def process_table(table, faction):
    data = []
    for row in table.find_all('tr'):
        entry = row.find_all('td')[1:-5]  # except first entry which is for image
        entry = [elem.text.strip().replace('—-', '') for elem in entry]
        entry.append(faction)
        data.append(entry)
    return data


def process_soup(soup):
    card_data = []
    leader_data = []
    for x, table in enumerate(soup.find_all('tbody')):
        if x < 5:
            table_data = process_table(table, faction_order[x])
            card_data += table_data
        else:
            table_data = process_table(table, faction_order[x % 5 + 1])
            leader_data += table_data
    return card_data, leader_data


faction_order = ('Neutral', 'Northen Relams', 'Nilfgaard', 'Scoia’tael', 'Monsters')
if __name__ == '__main__':
    cards, leaders = process_soup(get_soup('http://gwent-cards.com/'))
