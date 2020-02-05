from collections import OrderedDict, namedtuple
from Dip_Orders import Order, Create_Unit, Hold, Move, Support
from Dip_Env_Classes import Region, Army, Fleet


class Env:
    def __init__(self, nb_players):
        self.moves = {}
        self.units = {}
        self.strengths = {}
        self.results = {}
        self.regions = OrderedDict([
            ('Clyde', Region(name = 'Clyde', owner=0, supply=True,
                             unit=None, water=False, coastal=True, home=None,
                             neighbours=['Edinburgh', 'Liverpool', 'Yorkshire'])),
            ('Edinburgh', Region(name = 'Edinburgh', owner=0, supply=True,
                                 unit=None, water=False,
                                 coastal=True, home=0,
                                 neighbours=['Clyde', 'Liverpool', 'Yorkshire'])),
            ('Yorkshire', Region(name = 'Yorkshire', owner=None, supply=True,
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
        self.collect_orders(players)
        print('---FINDING CONFLICTS---')
        conflicts = self.find_conflicts()
        while conflicts:
            conflicts = self.resolve_conflicts(conflicts)
        for unit, order in self.moves.items():
            if type(order) == Move:
                self.results[unit] = order.to
            if type(order) == Hold or type(order) == Support:
                self.results[unit] = order.region
        print('RESULTS:', self.results)
        self.update_regions()


    def collect_orders(self, players):
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
            if type(order) == Hold or type(order) == Support:
                lst.append(order.region)
        return set([i for i in lst if lst.count(i)>1])


    def resolve_conflicts(self, conflicts):
        print('CONFLICTS:', conflicts)
        conflicting_region = conflicts.pop()
        conflicting_orders = self.get_conflicting_orders(conflicting_region)
        self.calculate_strengths()
        strongest_orders = [item for item in self.strengths.items() if \
                            item[1] == max(self.strengths.values())]

        print('CONFLICTING REGION:', conflicting_region)
        print('CONFLICTING ORDERS: ', conflicting_orders)
        print('STRENGTHS:', self.strengths)
        print('STRONGEST_ORDERS:', strongest_orders)

        if len(strongest_orders) == 1:
            strongest_unit, _ = strongest_orders[0]
            self.moves[strongest_unit].resolved = True
        for unit, order in conflicting_orders:
            if type(order) == Move and order.resolved == False:
                self.moves[unit].to = self.moves[unit].region

        return self.find_conflicts()


    def get_conflicting_orders(self, conflicting_region):
        conflicting_orders = []
        for unit, order in self.moves.items():
            if order.to == conflicting_region or \
            order.region == conflicting_region:
                conflicting_orders.append((unit, order))
        return conflicting_orders


    def calculate_strengths(self):
        for unit in self.moves:
            self.strengths[unit] = 1
        for unit, order in self.moves.items():
            if type(order) == Support:
                region = order.from_
                supported_unit = self.get_unit_by_region(region)
                self.strengths[supported_unit] += 1
            if type(order) == Move and self.regions[order.to].unit:
                affected_unit = self.get_unit_by_region(order.to)
                supported_unit = self.get_supported_unit(affected_unit)
                if type(self.moves[affected_unit]) == Support:
                    self.strengths[supported_unit] -= 1


    def get_supported_unit(self, unit):
        from_ = self.moves[unit].from_
        to = self.moves[unit].to
        for unit, order in self.moves.items():
            if order.region == from_ and order.to == to:
                return unit


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


    def get_unit_by_region(self, region):
        return hash(self.regions[region].unit) if \
        self.regions[region].unit else None
        

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
