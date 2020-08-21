class CreatureCard():
    def __init__(self, id, power, creature_type, name, is_hero=False, ability=None):
        self.id = id
        self.power = power
        self.power_bonus = 0
        self.power_multiplier = 1
        self.is_hero = is_hero
        self.creature_type = creature_type
        self.name = name
        self.ability = ability

    def __str__(self):
        print(str(self.get_power()))

    def get_power(self):
        return (self.power + self.power_bonus) * self.power_multiplier


class Army:
    def __init__(self):
        self.rows = [ArmyRow(), ArmyRow(), ArmyRow()]

    def place_card(self, *cards):
        for card in cards:
            self.rows[card.creature_type].place_card(card)

    def remove_card(self, *cards):
        for card in cards:
            self.rows[card.creature_type].remove_card(card)

    def get_cards_with_max_power(self):
        max_cards = [row.get_cards_with_max_power() for row in self.rows]
        max_power = max([row[0].get_power() for row in max_cards])
        cards = [row for row in max_cards if row[0] == max_power]
        return cards

    def get_power(self):
        return sum([row.get_power() for row in self.rows])

    def get_max_power(self):
        return max([row.get_max_power() for row in self.rows])

    def get_row(self, row_type=None):
        return self.rows[row_type] if row_type else self.rows

    def get_cards(self):
        return [row.get_cards() for row in self.rows]


class ArmyRow:
    def __init__(self):
        self.cards = []
        self.horn_multiplier = 1

    def place_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)

    def get_power(self):
        return sum([card.get_power() for card in self.cards]) * self.horn_multiplier

    def get_max_power(self):
        return max([card.get_power() for card in self.cards]) * self.horn_multiplier

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
