import config


class Card:
    def __init__(self, card_id, name, faction):
        self.id = card_id
        self.name = name
        self.faction = faction
        self.is_unit = False

    def __str__(self):
        return self.name


class AbilityCard(Card):
    def __init__(self, card_id, name, faction, abilities):
        super().__init__(card_id, name, faction)
        self.abilities = abilities


class LeaderCard(AbilityCard):
    def __init__(self, card_id, name, faction, abilities):
        super().__init__(card_id, name, faction, abilities)
        self.is_used = False


class UnitCard(AbilityCard):
    def __init__(self, card_id, name, faction, abilities, unit_type, power, is_hero):
        super().__init__(card_id, name, faction, abilities)
        self.power = power
        self.is_unit = True
        self.is_hero = is_hero
        self.unit_type = unit_type

        self.power_bonus = 0
        self.power_multiplier = 1
        self.row = None

    def get_power(self):
        if self.is_hero:
            return self.power
        else:
            power = (1 if self.row.bad_weather else self.power) + self.power_bonus
            return power * config.ABILITY_HORN_MULTIPLIER if self.row.horn_sources else power
