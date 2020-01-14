from Dip_Orders import Order, Create_Unit, Hold, Move, Support

class Player:
    def __init__(self, name, faction):
        self.name = name
        self.faction = faction
        self.units = []
        self.orders = []


if __name__ == '__main__':
    player1 = Player('Charles', 2)

    order1 = Create_Unit(2, 'Edin')
    print(order1.details())

    order2 = Move(2, 'Edin', to='Clyde')
    print(order2.details())

    
