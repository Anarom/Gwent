import config


class Card:
    def __init__(self, record):
        for key in record:
            setattr(self, key, record[key])
        self.is_unit = False

    def __str__(self):
        return self.name


class LeaderCard(Card):
    passives = ['emperor', 'extra_card']

    def __init__(self, record):
        super().__init__(record)
        self.passive = False
        self.order = 0
        self.used = False
        if record["ability"] in LeaderCard.passives:
            self.passive = True
            self.order = LeaderCard.passive.index(record["ability_name"])


class UnitCard(Card):
    def __init__(self, record):
        super().__init__(record)
        self.is_unit = True
        self.power_bonus = 0
        self.power_multiplier = 1
        self.row = None

    def get_power(self):
        if self.is_hero:
            return self.power
        else:
            power = (1 if self.row.bad_weather else self.power) + self.power_bonus
            return power * config.ABILITY_HORN_MULTIPLIER if self.row.horn_sources else power
