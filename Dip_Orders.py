class Order:
    def __init__(self, player, region, fleet=False, to=None):
        self.resolved = False
        self.player = player
        self.region = region
        self.fleet = None
        self.to = to

class Create_Army(Order):
    def details(self):
        return f'Player {self.player} creates army at {self.region}'

class Hold(Order):
    def details(self):
        return f'Player {self.player}\'s army at {self.region} holds'

class Move(Order):
    def details(self):
        return f'Player {self.player} moves army from {self.region} to {self.to}'

class Support(Order):
    def details(self):
        return f'Player {self.player}\'s army at {self.region} supports from \
        {self.from_} to {self.to}'
