class Player:
    def __init__(self, name, faction):
        self.name = name
        self.faction = faction
        self.armies = []


    def orders():
        pass


class Order:
    def __init__(self, region, player):
        self.region = region
        self.player = player


class Create_Army_Order(Order):
    def details(self, owner, fleet, region):
        self.army = Army(owner, fleet, region)
        
        

##class Hold_Order(Order):
##    pass


class Move_Order(Order):
    def details(self, from_, to):
        self.from_ = from_
        self.to = to
        print(f'Moving player {self.player}\'s army from {self.from_} to {self.to}')


##class Support_Order(Order):
##    pass


class Army:
    def __init__(self, owner, fleet, region):
        self.owner = owner
        self.fleet = fleet
        self.region = region



