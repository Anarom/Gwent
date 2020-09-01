import config


class Card:
    def __init__(self, card_id, name, faction):
        self.id = card_id
        self.name = name
        self.faction = faction


class AbilityCard(Card):
    def __init__(self, card_id, name, faction, abilities):
        super().__init__(card_id, name, faction)
        self.abilities = abilities


class UnitCard(AbilityCard):
    def __init__(self, card_id, name, faction, abilities, unit_type, power, power_type):
        super().__init__(card_id, name, faction, abilities)
        self.power = power
        self.power_type = power_type
        self.unit_type = unit_type

        self.power_bonus = 0
        self.power_multiplier = 1
        self.row = None

    def get_power(self):
        if self.power_type == 'normal':
            power = (1 if self.row.bad_weather else self.power) + self.power_bonus
            return power * config.ABILITY_HORN_MULTIPLIER if self.row.horn_active else power
        else:
            return self.power

    def __str__(self):
        return self.name
