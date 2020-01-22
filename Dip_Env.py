from collections import OrderedDict, namedtuple
from Dip_Orders import Order, Create_Unit, Hold, Move, Support
from Dip_Env_Classes import Region, Army, Fleet


class Env:
    def __init__(self, nb_players):
        self.moves = {}
        self.results = {}
        self.units = {}
        self.regions = OrderedDict([
            ('Clyde', Region(name = 'Clyde', owner=None, supply=False,
                             unit=None, water=False, coastal=True, home=None,
                             neighbours=['Edinburgh', 'Liverpool', 'Yorkshire'])),
            ('Edinburgh', Region(name = 'Edinburgh', owner=0, supply=True,
                                 unit=None, water=False,
                                 coastal=True, home=0,
                                 neighbours=['Clyde', 'Liverpool', 'Yorkshire'])),
            ('Yorkshire', Region(name = 'Yorkshire', owner=None, supply=False,
                                 unit=None, water=False, coastal=True, home=None,
                                 neighbours=['Clyde', 'Edinburgh', 'Liverpool'])),
            ('Liverpool', Region(name = 'Liverpool', owner=1, supply=True,
                                 unit=None, water=False,
                                 coastal=True, home=0,
                                 neighbours=['Clyde', 'Edinburgh', 'Yorkshire']))
            ])


    def resolve_builds(self, order_sheet):
        for order in order_sheet:
            if type(order) == Create_Unit:
                self.create_unit(order)


    def resolve_orders(self, players):
        for player in players:
            for unit in player.units:
                self.units[hash(unit)] = unit
                self.moves[hash(unit)] = unit.orders
        conflicts = self.find_conflicts()
        print('conflicts:', conflicts)
        for unit, order in self.moves.items():
            self.results[unit] = order.to
        self.update_regions()


    def find_conflicts(self):
        lst = [move.to for move in self.moves.values()]
        return set([i for i in lst if lst.count(i)>1])
        

    def update_regions(self):
        self.clear_all_regions()
        for unit, region in self.results.items():
            self.regions[region].unit = unit


    def clear_all_regions(self):
        for region in self.regions.values():
            region.unit = None
        

    def create_unit(self, order):
        if self.regions[order.region].supply == True and \
        self.regions[order.region].unit == None and \
        self.regions[order.region].owner == order.player:
            new_army = Army(order.player, order.region)
            self.regions[order.region].unit = new_army
            self.results[hash(new_army)] = (new_army, order.region, order.player)
   

    def reset_results(self):
        self.results = {}


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
