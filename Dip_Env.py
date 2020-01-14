from collections import OrderedDict, namedtuple
from Dip_Orders import Order, Create_Unit, Hold, Move, Support
from Dip_Env_Classes import Region, Army, Fleet


class Env:
    def __init__(self, nb_players):
        self.moves = OrderedDict([
            ('Clyde', []),
            ('Edinburgh', []),
            ('Yorkshire', []),
            ('Liverpool', [])
            ])
        self.regions = OrderedDict([
            ('Clyde', Region(name = 'Clyde', owner=None, supply=False,
                             unit=None, water=False, coastal=True, home=None,
                             neighbours=['Edinburgh', 'Liverpool', 'Yorkshire'])),
            ('Edinburgh', Region(name = 'Edinburgh', owner=0, supply=True,
                                 unit=None, water=False, coastal=True, home=0,
                                 neighbours=['Clyde', 'Liverpool', 'Yorkshire'])),
            ('Yorkshire', Region(name = 'Yorkshire', owner=None, supply=False,
                                 unit=None, water=False, coastal=True, home=None,
                                 neighbours=['Clyde', 'Edinburgh', 'Liverpool'])),
            ('Liverpool', Region(name = 'Liverpool', owner=1, supply=True,
                                 unit=None, water=False, coastal=True, home=0,
                                 neighbours=['Clyde', 'Edinburgh', 'Yorkshire']))
            ])


    def submit_orders(self, order_sheet):
        for order in order_sheet:
            if type(order) == Create_Unit:
                self.create_unit(order)
            if type(order) == Move:
                self.moves[order.to].append(order)


    def resolve_orders(self):
        self.results = {}
        print('self.moves:', self.moves)
        print(self.moves['Clyde'][0])
        order1 = self.moves['Clyde'][0]
        order2 = self.moves['Yorkshire'][0]
        self.move(order1)
        self.move(order2)


    def move(self, order): 
        self.regions[order.region].unit = None
        self.regions[order.to].unit = True


    def create_unit(self, order):
        if self.regions[order.region].supply == True and \
        self.regions[order.region].unit == None and \
        self.regions[order.region].owner == order.player:
            self.regions[order.region].unit = True


    def print_board(self):
        print('-----------------------')
        print('|  Clyde   |   Edin   |')
        print('|          |', end = '') if not self.regions['Clyde'].unit \
        else print('|    A     |', end = '')
        print('          |') if not self.regions['Edinburgh'].unit \
        else print('    A     |')
        print('-----------------------')
        print('| Yorkshire| Liverpool|')
        print('|          |', end = '') if not self.regions['Yorkshire'].unit \
        else print('|    A     |', end = '')
        print('          |') if not self.regions['Liverpool'].unit \
        else print('    A     |')
        print('-----------------------')


if __name__ == '__main__':
    place = Region(name = 'Sydney', owner=None, supply=False, unit=None,
                   water=False, coastal=True, home=None,
                   neighbours=['Edinburgh', 'Liverpool', 'Yorkshire'])
    #print(place)
    #print(place.army)




    

