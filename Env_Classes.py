class Region:
    def __init__(self, name, owner, supply, unit, water, coastal, home, neighbours):
        self.name = name
        self.owner = owner
        self.supply = supply
        self.unit = unit
        self.water = water
        self.coastal = coastal
        self.home = home
        self.neighbours = neighbours


class Army:
    def __init__(self, owner, region):
        self.orders = None
        self.owner = owner
        self.region = region


class Fleet:
    def __init__(self, owner, region):
        self.orders = None
        self.owner = owner
        self.region = region
