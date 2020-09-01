import random
import json
from card import AbilityCard, UnitCard


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
        self.unit_cards = []
        self.special_cards = []
        with open('cards.json', 'r', encoding='utf-8') as file:
            card_records = json.load(file)
        with open('leaders.json', 'r', encoding='utf-8') as file:
            self.leaders = json.load(file)
        for record in card_records:
            if record['card_type'] < 3:  # card in unit
                card = UnitCard(record['id'], record['name'], record['faction'], record['card_type'],
                                record['abilities'], record['power'], record['power_type'])
                self.unit_cards.append(card)
            elif record['card_type'] == 3:
                card = AbilityCard(record['id'], record['name'], record['faction'], record['abilities'])
                self.special_cards.append(card)
