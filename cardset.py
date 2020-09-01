import random
import json
from card import AbilityCard, UnitCard
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


class CardLib:
    def __init__(self):
        self.unit_cards = {'Northen Relams': [], 'Neutral': [], 'Nilfgaardian Empire': [],
                           "Scoia'tael": [], 'Monsters': []}
        self.special_cards = []
        with open('cards.json', 'r', encoding='utf-8') as file:
            card_records = json.load(file)
        with open('leaders.json', 'r', encoding='utf-8') as file:
            self.leaders = json.load(file)
        for record in card_records:
            if record['card_type'] < 3:  # card in unit
                card = UnitCard(record['id'], record['name'], record['faction'], record['card_type'],
                                record['abilities'], record['power'], record['power_type'])
                self.unit_cards[record['faction']].append(card)
            elif record['card_type'] == 3:
                card = AbilityCard(record['id'], record['name'], record['faction'], record['abilities'])
                self.special_cards.append(card)

    def generate_deck(self, faction, s_card_amount=random.randint(0, config.DECK_SPECIAL_CARD_LIMIT)):
        if s_card_amount > config.DECK_SPECIAL_CARD_LIMIT:
            print(f'Maximum amount of special cards exceeded ({config.DECK_SPECIAL_CARD_LIMIT})')
            return []
        s_cards = random.choices(self.special_cards, k=s_card_amount)
        u_cards = random.choices(self.unit_cards[faction], k=config.DECK_UNIT_CARD_AMOUNT)
        return s_cards + u_cards
