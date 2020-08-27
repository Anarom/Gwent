import config


class CreatureCard():
    def __init__(self, card_id, power, creature_type, name, power_type='normal', abilities=None):
        self.id = card_id
        self.power = power
        self.power_bonus = 0
        self.power_multiplier = 1
        self.power_type = power_type
        self.creature_type = creature_type
        self.name = name
        self.abilities = abilities

        self.row = None

    def get_power(self):
        if self.power_type == 'normal':
            power = (1 if self.row.bad_weather else self.power) + self.power_bonus
            return power * config.ABILITY_HORN_MULTIPLIER if self.row.horn_active else power
        else:
            return self.power

    def __str__(self):
        print(str(self.get_power()))


class Army:
    def __init__(self):
        self.rows = [ArmyRow(), ArmyRow(), ArmyRow()]

    def place_card(self, card):
        self.rows[card.creature_type].place_card(card)

    def remove_card(self, card):
        self.rows[card.creature_type].remove_card(card)

    def get_cards_with_max_power(self):
        max_cards = [row.get_cards_with_max_power() for row in self.rows]
        max_power = max([row[0].get_total_power() for row in max_cards])
        cards = [row for row in max_cards if row[0] == max_power]
        return cards

    def get_total_power(self):
        return sum([row.get_total_power() for row in self.rows])

    def get_max_power(self):
        return max([row.get_max_power() for row in self.rows])

    def get_row(self, row_type):
        return self.rows[row_type]

    def get_cards(self):
        return [row.get_cards() for row in self.rows]


class ArmyRow:
    def __init__(self):
        self.cards = []
        self.horn_active = False
        self.bad_weather = False

    def place_card(self, card):
        self.cards.append(card)
        card.row = self

    def remove_card(self, card):
        self.cards.remove(card)
        card.row = None

    def get_total_power(self):
        return sum([card.get_power() for card in self.cards])

    def get_max_power(self):
        return max([card.get_power() for card in self.cards])

    def get_cards(self):
        return self.cards

    def get_cards_with_max_power(self):
        max_power = self.get_max_power()
        cards = [card for card in self.cards if card.get_power() == max_power]
        return cards


class Board:
    def __init__(self):
        self.armies = [Army(), Army()]
        self.weather = []


class Game:
    def __init__(self, *players):
        self.board = Board()
        self.players = players
        for player_id, player in enumerate(self.players):
            player.player_id = player_id
            player.army = self.board.armies[player_id]
            player.opponent = self.players[1 - player_id]
