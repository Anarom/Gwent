class Army:
    def __init__(self):
        self.rows = [ArmyRow(), ArmyRow(), ArmyRow()]

    def place_card(self, card):
        self.rows[card.creature_type].place_card(card)

    def remove_card(self, card):
        self.rows[card.creature_type].remove_card(card)

    def get_total_power(self):
        return sum([row.get_total_power() for row in self.rows])

    def get_max_power(self):
        return max([row.get_max_power() for row in self.rows])

    def get_rows(self, row_type=None):
        return self.rows[row_type] if row_type else self.rows

    def get_cards(self, power=None):
        return [row.get_cards(power) for row in self.rows]


class ArmyRow:
    def __init__(self):
        self.cards = []
        self.horn_sources = []
        self.bad_weather = False

    def place_card(self, card):
        self.cards.append(card)
        card.row = self

    def remove_card(self, card):
        self.cards.remove(card)
        card.row = None
        if card in self.horn_sources:
            self.horn_sources.remove(card)

    def get_total_power(self):
        return sum([card.get_power() for card in self.cards])

    def get_max_power(self):
        return max([card.get_power() for card in self.cards if not card.is_hero])

    def get_cards(self, power):
        return [card for card in self.cards if card.get_power() == power]


class Board:
    def __init__(self):
        self.armies = [Army(), Army()]
        self.weather = []
