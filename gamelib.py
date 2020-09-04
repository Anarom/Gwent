import random
import json
from game import Game
import config
from card import Card, LeaderCard, UnitCard


class GameLib(Game):
    def __init__(self):

        self.units = {}
        self.leaders = {}
        self.special_cards = []
        for faction in Game.factions:
            self.units[faction] = []
            self.leaders[faction] = []
        self.import_data()

    def import_data(self):
        with open('cards.json', 'r', encoding='utf-8') as file:
            records = json.load(file)
        for record in records:
            if record['card_type'] < 3:  # card is unit
                card = UnitCard(record)
                self.units[record['faction']].append(card)
            elif record['card_type'] == 3:  # card is special
                card = Card(record)
                self.special_cards.append(card)
            else:  # card is leader
                card = LeaderCard(record)
                self.leaders[record['faction']].append(card)

    def generate_deck(self, faction, s_card_amount=random.randint(0, config.DECK_SPECIAL_CARD_LIMIT)):
        if s_card_amount > config.DECK_SPECIAL_CARD_LIMIT:
            print(f'Maximum amount of special cards exceeded ({config.DECK_SPECIAL_CARD_LIMIT})')
            return []
        s_cards = random.choices(self.special_cards, k=s_card_amount)
        u_cards = random.choices(self.units[faction], k=config.DECK_UNIT_CARD_AMOUNT)
        return s_cards + u_cards


if __name__ == '__main__':
    lib = GameLib()
