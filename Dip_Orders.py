class Order:
    def __init__(self, player, region, fleet=False, from_=None, to=None):
        self.resolved = False
        self.player = player
        self.region = region
        self.fleet = fleet
        self.from_ = from_
        self.to = to


class Create_Unit(Order):
    def details(self):
        return f'Player {self.player} creates unit at {self.region}'


class Hold(Order):
    def details(self):
        return f'Player {self.player}\'s unit at {self.region} holds'


class Move(Order):
    def details(self):
        return f'Player {self.player} moves unit from {self.region} to {self.to}'


class Support(Order):
    def details(self):
        return f'Player {self.player}\'s unit at {self.region} supports from \
{self.from_} to {self.to}'
