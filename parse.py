import requests
import json
from bs4 import BeautifulSoup


def id_generator():
    x = 1
    while True:
        yield x
        x += 1
        

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def process_table(table, faction):
    data = []
    for row in table.find_all('tr'):
        attrs = row.find_all('td')[1:-5]  # except first entry which is for image
        attrs = [elem.text.strip().replace('—-', '') for elem in attrs]
        entry = {}
        for x, attr in enumerate(attrs):
            entry[card_attrs[x]] = attr if attr else None
        entry['faction'] = faction
        entry['id'] = next(id_gen)
        data.append(entry)
    return data


def process_soup(soup):
    card_data = []
    leader_data = []
    for x, table in enumerate(soup.find_all('tbody')):
        if x < 5:  # card processing
            table_data = process_table(table, faction_order[x])
            for entry in table_data:
                entry['is_hero'] = bool(entry['is_hero'])
                entry['power'] = int(entry['power']) if entry['power'] else None
                if entry['name'] in weather_cards:
                    entry['card_type'] = 'weather'
                elif entry['name'] in special_cards:
                    entry['card_type'] = 'special'
                else:
                    entry['card_type'] = 'unit'
            card_data += table_data
        else:  # leader processing
            table_data = process_table(table, faction_order[x % 5 + 1])
            for entry in table_data:
                del entry['power']
                entry['card_type'] = 'leader'
            leader_data += table_data
    return card_data, leader_data


def dump_to_file(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=1, sort_keys=True)


faction_order = ('Neutral', 'Northen Relams', 'Nilfgaard', 'Scoia’tael', 'Monsters')
card_attrs = ('name', 'power', 'ability', 'is_hero')
weather_cards = ('Biting Frost', 'Impenetrable Fog', 'Torrential Rain', 'Clear Weather')
special_cards = ('Decoy', 'Scorch', 'Commander’s Horn')

if __name__ == '__main__':
    id_gen = id_generator()
    cards, leaders = process_soup(get_soup('http://gwent-cards.com/'))
    dump_to_file(cards, 'cards.json')
    dump_to_file(leaders, 'leaders.json')
