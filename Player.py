from cardset import CardSet
import config


class Player:

    def __init__(self, deck_cards):
        self.deck = CardSet(deck_cards)
        self.hand = CardSet()
        self.discard_pile = CardSet()
        self.army = None
        self.opponent = None
        self.leader_used = False

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


cards = [x for x in range(1, 31)]
p = Player(cards)
p.draw_hand()
