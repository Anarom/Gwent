import random
import json
from card import AbilityCard, LeaderCard, UnitCard
import config


class CardSet:
    def __init__(self, cards=None):
        self.cards = []
        if cards:
            for card in cards:
                self.add_card(card)

    def add_card(self, card):
        self.cards.append(card)

    def draw_card(self, card_id=None):
        if card_id:
            card = None
            for card in self.cards:
                if card.id == card_id:
                    break
        else:
            card = random.choice(self.cards)
        self.cards.remove(card)
        return card

    def choose_card(self):
        self.print()
        response = int(input()) - 1
        card = self.cards[response]
        self.cards.remove(card)
        return card

    def get_cards(self):
        return self.cards

    def swap_card(self, index, new_card):
        old_card = self.cards[index]
        self.cards[index] = new_card
        return old_card

    def reset(self):
        self.cards = []

    def get_size(self):
        return len(self.cards)

    def print(self):
        for card in self.cards:
            print(card, end=' ')
        print()


class GameLib:
    def __init__(self):
        self.factions = ['Northen Relams', 'Nilfgaardian Empire', "Scoia'tael", 'Monsters', 'Neutral']
        self.units = {}
        self.leaders = {}
        self.special_cards = []
        for faction in self.factions:
            self.units[faction] = []
            self.leaders[faction] = []
        self.import_data()

    def import_data(self):
        with open('cards.json', 'r', encoding='utf-8') as file:
            records = json.load(file)
        for record in records:
            if record['card_type'] < 3:  # card is unit
                card = UnitCard(record['id'], record['name'], record['faction'], record['abilities'],
                                record['card_type'], record['power'], record['power_type'])
                self.units[record['faction']].append(card)
            elif record['card_type'] == 3:  # card is special
                card = AbilityCard(record['id'], record['name'], record['faction'], record['abilities'])
                self.special_cards.append(card)
            else:  # card is leader
                card = LeaderCard(record['id'], record['name'], record['faction'], record['abilities'])
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
