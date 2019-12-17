class Region:
    def __init__(self, name, owner, supply, army, water, coastal, home, neighbours):
        self.name = name
        self.owner = owner
        self.supply = supply
        self.army = army
        self.water = water
        self.coastal = coastal
        self.home = home
        self.neighbours = neighbours


class Army:
    def __init__(self, owner, region):
        self.owner = owner
        self.region = region


class Fleet:
    def __init__(self, owner, region):
        self.owner = owner
        self.region = region
