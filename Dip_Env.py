from collections import OrderedDict, namedtuple
from Dip_Orders import Order, Create_Army, Hold, Move, Support
from Dip_Env_Classes import Region, Army, Fleet


class Env:
    def __init__(self, nb_players):
        self.moves = OrderedDict([
            ('Clyde', [0 for i in range(nb_players)]),
            ('Edinburgh', [0 for i in range(nb_players)]),
            ('Yorkshire', [0 for i in range(nb_players)]),
            ('Liverpool', [0 for i in range(nb_players)])
            ])
        self.regions = OrderedDict([
            ('Clyde', Region(name = 'Clyde', owner=None, supply=False,
                             army=None, water=False, coastal=True, home=None,
                             neighbours=['Edinburgh', 'Liverpool', 'Yorkshire'])),
            ('Edinburgh', Region(name = 'Edinburgh', owner=0, supply=True,
                                 army=None, water=False, coastal=True, home=0,
                                 neighbours=['Clyde', 'Liverpool', 'Yorkshire'])),
            ('Yorkshire', Region(name = 'Edinburgh', owner=None, supply=False,
                                 army=None, water=False, coastal=True, home=None,
                                 neighbours=['Clyde', 'Edinburgh', 'Liverpool'])),
            ('Liverpool', Region(name = 'Liverpool', owner=1, supply=True,
                                 army=None, water=False, coastal=True, home=0,
                                 neighbours=['Clyde', 'Edinburgh', 'Yorkshire']))
            ])


    def submit_orders(self, order_sheet):
        for order in order_sheet:
            if type(order) == Create_Army:
                self.create_army(order)
            if type(order) == Move:
                self.move(order)
                #self.lodge_move(order)


    def lodge_move(self, order):
        self.moves[order.region][order.player] += 1


    def resolve_orders(self):
        # check if two people aren't moving into the same space
        for region in self.moves:
            max_strength = [i for i, x in enumerate(self.moves[region]) \
                            if x == max(self.moves[region])]
            # print(max_strength)
            # result [0] means player 0 has the most strength to move into that
            # region
            # approve player 0 to move into Edinburgh
            # approve player 1 to move into Liverpool
            


    def move(self, order):
        self.regions[order.region].army = None
        self.regions[order.to].army = True


    def create_army(self, order):
        if self.regions[order.region].supply == True and \
        self.regions[order.region].army == None and \
        self.regions[order.region].owner == order.player:
            self.regions[order.region].army = True


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
    #print(place)
    #print(place.army)

    new_dict = OrderedDict([])
    with open('regions.txt', 'r') as file:
        for line in file:
            line = line.strip('\n')
            print(line.split(' ', 1))
            #new_dict.update
    





    

