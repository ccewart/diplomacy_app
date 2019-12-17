from collections import OrderedDict, namedtuple
from Dip_Orders import Order, Create_Army, Hold, Move, Support


Region = namedtuple('Region', 'name owner supply army water coastal home neighbours')
Army = namedtuple('Army', 'owner region')
Fleet = namedtuple('Fleet', 'owner region')


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


class Env:
    def __init__(self):
        self.regions = OrderedDict([
            ('Clyde', Region(name = 'Clyde', owner=None, supply=False, army=None,
                             water=False, coastal=True, home=None,
                             neighbours=['Edinburgh', 'Liverpool', 'Yorkshire'])),
            ('Edinburgh', Region(name = 'Edinburgh', owner=0, supply=True, army=None,
                                 water=False, coastal=True, home=0,
                                 neighbours=['Clyde', 'Liverpool', 'Yorkshire'])),
            ('Yorkshire', Region(name = 'Edinburgh', owner=None, supply=False, army=None,
                                 water=False, coastal=True, home=None,
                                 neighbours=['Clyde', 'Edinburgh', 'Liverpool'])),
            ('Liverpool', Region(name = 'Liverpool', owner=1, supply=True, army=None,
                                 water=False, coastal=True, home=0,
                                 neighbours=['Clyde', 'Edinburgh', 'Yorkshire']))
            ])


    def resolve_orders(self, order_sheet):
        for order in order_sheet:
            if type(order) == Create_Army:
                if self.regions[order.region].supply == True and \
                self.regions[order.region].army == None and \
                self.regions[order.region].owner == order.player:
                    print('   ', order.player)
                    print('   ', order.region)
                    print('   ', self.regions[order.region])
                    
                    self.regions[order.region].army = True


    def lodge_move(self, from_, to, owner):
        print(self.regions[from_].army.owner)
        print(owner)
        #if self.regions[from_].army.owner = owner:


    def move_army(move_arg):
        if type(move_arg) == Move_Order:
            print('Can move')


    def create_army(self, owner, type_, region):
        if not self.regions[region].army and self.regions[region].supply:
            if type_ == 'army':
                self.regions[region].army = Army(owner, False, region) 
            else:
                self.regions[region].army = Army(owner, True, region)


    def print_board(self):
        print('-----------------------')
        print('|  Clyde   |   Edin   |')
        print('|          |', end = '') if not self.regions['Clyde'].army \
        else print('|    A     |', end = '')
        print('          |') if not self.regions['Edinburgh'].army \
        else print('    A     |')
        print('-----------------------')
        print('| Yorkshire| Liverpool|')
        print('|          |', end = '') if not self.regions['Yorkshire'].army \
        else print('|    A     |', end = '')
        print('          |') if not self.regions['Liverpool'].army \
        else print('    A     |')
        print('-----------------------')


if __name__ == '__main__':
    place = Region(name = 'Sydney', owner=None, supply=False, army=None,
                   water=False, coastal=True, home=None,
                   neighbours=['Edinburgh', 'Liverpool', 'Yorkshire'])

    
    print(place)
    print(place.army)
    





    

