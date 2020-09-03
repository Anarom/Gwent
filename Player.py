from cardset import CardSet
import config


class Player:
    def __init__(self, deck, leader):
        self.deck = CardSet(deck)
        self.hand = CardSet()
        self.leader = leader
        self.discard_pile = CardSet()
        self.army = None

    def play_card(self, card):
        callbacks = []
        if card.abilities:
            for ability in card.abilities:
                callbacks.append(ability.apply(card))
            if True not in callbacks:
                self.army.place_card(card)

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

    def choose_row(self):
        pass

    def choose_unit(self):
        pass
