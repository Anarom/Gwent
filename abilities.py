import config


class Ability:
    game = None

    def __init__(self, ability_attrs=None):
        self.source_card = None
        self.player = Ability.game.active_player
        self.ability_triggers = {'Morale': self.morale, 'Medic': self.medic, 'Scorch': self.scorch, 'Agile': self.agile,
                                 'muster': self.muster, 'Spy': self.spy, 'Bond': self.tight_bond, 'Decoy': self.decoy}
        self.ability_attrs = ability_attrs

    def apply(self, source_card):
        self.source_card = source_card
        self.ability_triggers[self.source_card.ability]()

    # ability implementations
    # return True if source card placement is being controlled by ability method
    def morale(self):
        row = self.player.army.get_row(self.source_card.creature_type)
        for card in row.get_cards():
            if card is not self.source_card and not card.is_hero:
                card.power_bonus += 1

    def medic(self):
        self.player.army.place_card(self.source_card)
        self.player.play_card(self.player.discard_pile.choose_card())
        return True  # source card is not placed in player.play_card()

    def scorch(self):
        if not self.ability_attrs:
            player_power = self.player.army.get_max_power()
            opponent_power = self.player.opponent.army.get_max_power()
            if player_power >= opponent_power:
                for card in self.player.army.get_cards_with_max_power():
                    self.player.remove_card(card)
                if player_power == opponent_power:
                    for card in self.player.opponent.army.get_cards_with_max_power():
                        self.player.opponent.remove_card(card)
            else:
                for card in self.player.opponent.army.get_cards_with_max_power():
                    self.player.opponent.remove_card(card)
        else:  # ability attr = row_type
            row = self.player.opponent.army.get_row(self.ability_attrs)
            if row.get_total_power() >= config.ABILITY_SCORCH_ROW_POWER:
                for card in row.get_cards_with_max_power():
                    self.player.opponent.remove_card(card)

    def spy(self):
        self.player.opponent.army.place_card(self.source_card)
        for n in range(config.ABILITY_SPY_DRAW):
            self.player.hand.add_card(self.player.deck.draw_card())
        return True

    def tight_bond(self):
        row = self.player.army.get_row(self.source_card.creature_type)
        cards = [card for card in row.get_cards() if card.name == self.source_card.name]
        multiplier = len(cards) + 1
        for card in cards:
            card.power_multiplier = multiplier

    def agile(self):
        self.source_card.creature_type = self.player.choose_row()  # row numbering is equal to creature type numbering

    def muster(self):
        additional_bounds = {
            165: [166, 167, 168]}  # Arachas Behemoth
        source_name = self.source_card.name.split(':')[0]
        cards = [card for card in self.player.deck.get_cards() if card.name.split(':')[0] == source_name]
        if self.source_card.id in additional_bounds:
            for card_id in additional_bounds[self.source_card.id]:
                card_drawn = True
                card = None
                while card_drawn:
                    card = self.player.deck.draw_card(card_id=card_id)
                    if card:
                        cards.append(card)
                    else:
                        card_drawn = False
        for card in cards:
            self.player.army.place_card(card)
