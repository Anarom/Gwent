import random


class CardSet:
    def __init__(self, cards=None):
        self.cards = []
        if cards:
            for card in cards:
                self.add_card(card)

    def add_card(self, card):
        self.cards.append(card)

    def draw_card(self, specific_card=None, card_id=None):
        if specific_card:
            card = specific_card
        elif card_id:
            for card in self.cards:
                if card.id == card_id:
                    break
        else:
            card = random.choice(self.cards)
        self.cards.remove(card)
        return card

    def get_cards(self, amount=None):
        if amount:
            return random.choices(self.cards, k=amount)
        else:
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
