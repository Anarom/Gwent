class CreatureCard():
    def __init__(self, power, creature_type, name, effects=[]):
        self.power = power
        self.creature_type = creature_type
        self.name = name
        self.effects = effects


class BoardRow:
    def __init__(self, creature_type):
        self.creature_type = creature_type
        self.cards = []
        self.effects = []


class Army:
    def __init__(self, player_id):
        self.player_id = player_id
        self.melee_row = BoardRow(0)
        self.ranged_row = BoardRow(1)
        self.siege_row = BoardRow(2)

class Board:
    def __init__(self):
        self.armies = (Army(0),Army(1))
        self.effects = []