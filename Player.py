class Player:
    def __init__(self, name, faction):
        self.name = name
        self.faction = faction
        self.units = []
        self.orders = []