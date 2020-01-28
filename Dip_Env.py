from collections import OrderedDict, namedtuple
from Dip_Orders import Order, Create_Unit, Hold, Move, Support
from Dip_Env_Classes import Region, Army, Fleet


class Env:
    def __init__(self, nb_players):
        self.moves = {}
        self.results = {}
        self.units = {}
        self.regions = OrderedDict([
            ('Clyde', Region(name = 'Clyde', owner=0, supply=True,
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
        self.collect_moves(players)
        conflicts = self.find_conflicts()

        while conflicts:
            print('moves:', self.moves)
            conflicts = self.find_conflicts()
            self.resolve_conflicts(conflicts)
            print()
        for unit, order in self.moves.items():
            if type(order) == Move:
                self.results[unit] = order.to
            if type(order) == Hold:
                self.results[unit] = order.region
        print('results:', self.results)
        self.update_regions()


    def collect_moves(self, players):
        for player in players:
            for unit in player.units:
                if unit.orders == None:
                    unit.orders = Hold(player, unit.region)
                self.units[hash(unit)] = unit
                self.moves[hash(unit)] = unit.orders


    def find_conflicts(self):
        lst = []
        for order in self.moves.values():
            if type(order) == Move:
                lst.append(order.to)
            if type(order) == Hold:
                lst.append(order.region)
        return set([i for i in lst if lst.count(i)>1])


    def resolve_conflicts(self, conflicts):
        print('conflicts:', conflicts)
        conflicting_orders = [move for move in self.moves.items() \
                              if move[1].to in conflicts \
                              or move[1].region in conflicts]
        print('conflicting orders: ', conflicting_orders)
        # to do: check for supports

        # liverpool and clyde 
        for unit, _ in conflicting_orders:
            self.moves[unit].to = self.moves[unit].region
        

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
