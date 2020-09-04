from cardset import CardSet
import config


class Player:
    def __init__(self, deck, leader):
        self.deck = CardSet(deck)
        self.hand = CardSet()
        self.leader = leader
        self.discard_pile = CardSet()
        self.army = None
        self.passive_abilities = []

    def play_card(self, card):
        callbacks = []
        if card.ability:
            if len(card.ability) > 1:
                for ability in card.ability:
                    callbacks.append(ability.apply(card))
            else:
                callbacks.append(card.ability.apply(card))
            if True not in callbacks and card.is_unit:
                self.army.place_card(card)

    def remove_card(self, card, in_hand=False):
        self.army.remove_card(card)
        pile = self.hand if in_hand else self.discard_pile
        pile.add_card(card)

    def play_leader(self):
        self.leader.used = True
        self.leader.ability.apply()

    def draw_hand(self):
        # initial draw
        self.hand.reset()
        for card_num in range(config.PLAYER_HAND_SIZE):
            self.hand.add_card(self.deck.draw_card())
        # swap cards
        for cards_changed in range(config.PLAYER_CARD_CHANGE_LIMIT):
            self.hand.print()
            response = int(input()) - 1
            if response in range(self.hand.get_size()):
                old_card = self.hand.swap_card(response, self.deck.draw_card())
                self.deck.add_card(old_card)

    def view_cards(self, cards):
        pass

    def select_row(self):
        pass

    def select_unit(self):
        pass
