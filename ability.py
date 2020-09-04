import config
from game import Game


class GameAbility(Game):

    def __init__(self, ability_name, param=None):
        self.src = None
        self.method = getattr(self, ability_name)
        self.param = param

    def apply(self, source_card):
        self.src = source_card
        self.method()

    # method returns True if src placement is being controlled by it
    def morale(self):
        row = self.host.army.get_rows(row_type=self.src.unit_type)
        for card in row.get_cards():
            if not card.is_hero:
                card.power_bonus += 1

    def medic(self):
        self.host.army.place_card(self.src)
        self.host.play_card(self.host.discard_pile.select_card())
        return True

    def scorch(self):
        if not self.param:  # special card
            max_power = max(self.host.army.get_max_power(), self.opp.army.get_max_power())
            for side in (self.host, self.opp):
                for card in side.army.get_cards(power=max_power):
                    if not card.is_hero:
                        side.remove_card(card)
            return True
        else:  # unit card
            row = self.opp.army.get_rows(row_type=self.param)
            if row.get_total_power() >= config.ABILITY_SCORCH_ROW_POWER:
                for card in row.get_cards(power=row.get_max_power()):
                    if not card.is_hero:
                        self.opp.remove_card(card)

    def spy(self):
        self.opp.army.place_card(self.src)
        for _ in range(config.ABILITY_SPY_DRAW):
            self.host.hand.add_card(self.host.deck.draw_card())
        return True

    def bond(self):
        self.host.army.place_card(self.src)
        row = self.host.army.get_rows(row_type=self.src.unit_type)
        cards = [card for card in row.get_cards() if card.name == self.src.name]
        for card in cards:
            card.power_multiplier = len(cards)

    def agile(self):
        self.src.unit_type = self.host.select_row()  # row numbering is equal to unit type numbering

    def muster(self):
        additional_bounds = {
            165: [166, 167, 168]}  # Arachas Behemoth
        source_name = self.src.name.split(':')[0]
        cards = [card for card in self.host.deck.get_cards() if card.name.split(':')[0] == source_name]
        if self.src.id in additional_bounds:
            for card_id in additional_bounds[self.src.id]:
                card_drawn = True
                while card_drawn:
                    card = self.host.deck.draw_card(card_id=card_id)
                    if card:
                        cards.append(card)
                    else:
                        card_drawn = False
        for card in cards:
            self.host.army.place_card(card)  # probably can play it not just place

    def horn(self):
        if self.src.is_unit:
            row = self.host.army.get_rows(row_type=self.src.unit_type)
        else:
            row = self.host.select_row()
        row.horn_sources.append(self.src)

    # special exclusive abilities
    def decoy(self):
        self.host.remove_card(self.host.select_unit(), in_hand=True)

    def bad_weather(self):
        if self.param not in self.board.weather:
            self.board.weather.append(self.param)
        for side in (self.host, self.opp):
            row = side.get_rows(row_type=self.param)
            row.bad_weather = True

    def clear_weather(self):
        self.board.weather = []
        for side in (self.host, self.opp):
            for row in side.get_rows():
                row.bad_weather = False
