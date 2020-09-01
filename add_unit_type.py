import json

unit_types = {'melee': 0, 'ranged': 1, 'siege': 2}
json_file = 'cards.json'
for unit_type in unit_types:
    units = []
    with open(f'{unit_type}.txt', 'r', encoding='utf-8') as file:
        for line in file:
            units.append(line[:-1])

    with open(json_file, 'r', encoding='utf-8') as file:
        cards = json.load(file)

    for unit in units:
        for card in cards:
            if card['name'] == unit and card['card_type'] in ('unit', 'special'):
                card['card_type'] = unit_types[unit_type]

    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(cards, file, sort_keys=True, ensure_ascii=False, indent=1)
