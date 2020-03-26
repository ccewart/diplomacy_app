from collections import OrderedDict, namedtuple
from Dip_Orders import Order, Create_Unit, Hold, Move, Support
from Dip_Env_Classes import Region, Army, Fleet


class Env:
    def __init__(self, nb_players):
        self.moves = {}
        self.units = {}
        self.strengths = {}
        self.results = {}
        self.dislodged = {}
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
                                 neighbours=['Clyde', 'Edinburgh', 'Yorkshire'])),
            ('Norwegian Sea', Region(name = 'Norwegian Sea', owner=1, supply=True,
                                 unit=None, water=False,
                                 coastal=True, home=0,
                                 neighbours=['Edinburgh', 'Liverpool'])),
            ('North Sea', Region(name = 'Liverpool', owner=1, supply=True,
                                 unit=None, water=False,
                                 coastal=True, home=0,
                                 neighbours=['Edinburgh', 'Liverpool']))
            ])


    def resolve_builds(self, order_sheet):
        '''
        Create units from orders
        '''
        for order in order_sheet:
            if type(order) == Create_Unit:
                self.create_unit(order)

    def collect_orders(self, players):
        for player in players:
            for unit in player.units:
                if unit.orders == None:
                    unit.orders = Hold(player, unit.region)
                self.units[hash(unit)] = unit
                self.moves[hash(unit)] = unit.orders


    def resolve_orders(self, players):
        '''

        '''
        self.collect_orders(players)
        self.cut_support()
        
        conflicts = self.find_conflicts()
        while conflicts:
            conflicts = self.resolve_conflicts(conflicts)
        for unit, order in self.moves.items():
            if type(order) == Move:
                self.results[unit] = order.to
            if type(order) == Hold or type(order) == Support:
                self.results[unit] = order.region
        print('RESULTS:', self.results)
        print('DISLODGED:', self.dislodged)
        self.update_regions()


    def find_conflicts(self):
        lst = []
        for unit, order in self.moves.items():
            if type(order) == Move and order.resolved == False:
                lst.append(order.to)
                
                # case when units are moving into each other
                targeted_unit = self.get_unit_by_region(order.to)
                if targeted_unit:
                    if self.moves[targeted_unit].to == order.region \
                       and unit != targeted_unit:
                        lst.append(order.to)
            if type(order) == Hold or type(order) == Support:
                lst.append(order.region)
        return set([i for i in lst if lst.count(i)>1])


    def resolve_conflicts(self, conflicts):
        print('CONFLICTS:', conflicts)
        conflicting_region = conflicts.pop()
        conflicting_orders = self.get_conflicting_orders(conflicting_region)
        local_strengths = self.calculate_local_strengths(conflicting_region,\
                                                         conflicting_orders)
        strongest_orders = [item for item in local_strengths.items() if \
                            item[1] == max(local_strengths.values())]

        print('  LOCAL STRENGTHS:', local_strengths)
        print('  STRONGEST_ORDERS:', strongest_orders)
        
        # unoccupied space, move successful
        if len(strongest_orders) == 1:
            strongest_unit = strongest_orders[0][0]
            self.moves[strongest_unit].resolved = True
        
        # unit dislodged, remove their orders from conflicting_orders
        conflicting_orders = self.resolve_dislodges(conflicting_region, \
                                            conflicting_orders, strongest_orders)

        # bounce unresolved move orders
        self.resolve_unsuccessful_moves(conflicting_orders)

        return self.find_conflicts()


    def resolve_dislodges(self, conflicting_region, conflicting_orders, \
                         strongest_orders):
        if len(strongest_orders) == 1 and self.regions[conflicting_region].unit:
            strongest_unit = strongest_orders[0][0]
            dislodged_unit = hash(self.regions[conflicting_region].unit)
            self.moves[strongest_unit].resolved = True
            dislodged_moves = self.moves.pop(dislodged_unit)
            self.dislodged[dislodged_unit] = dislodged_moves
            conflicting_orders = [item for item in conflicting_orders if item[0]\
                                  not in [key for key in self.dislodged.keys()]]
        return conflicting_orders


    def resolve_unsuccessful_moves(self, conflicting_orders):
        for unit, order in conflicting_orders:
            if type(order) == Move and order.resolved == False:
                affected_unit = self.get_unit_by_region(order.to)
                self.moves[unit].to = self.moves[unit].region
                if affected_unit:
                    # case when moving into a Move order, supports update
                    if type(self.moves[affected_unit]) == Move:
                        supporting_orders = self.get_supporting_orders(order.region)
                        for order in supporting_orders:
                            order.to = self.moves[unit].to


    def cut_support(self):
        for unit, order in self.moves.items():
            supporting_regions = self.get_supporting_regions(order.region)
            if type(order) == Move and self.regions[order.to].unit:
                affected_unit = self.get_unit_by_region(order.to)
                supported_unit = self.get_supported_unit(affected_unit)
                if type(self.moves[affected_unit]) == Support and supported_unit:
                    if self.moves[supported_unit].to != order.region:
                        self.moves[affected_unit].from_ = None
                        self.moves[affected_unit].to = None


    def get_conflicting_orders(self, conflicting_region):
        conflicting_orders = []
        for unit, order in self.moves.items():
            if order.to == conflicting_region or \
            order.region == conflicting_region:
                conflicting_orders.append((unit, order))
            elif type(order) == Support and order.from_ == conflicting_region:
                conflicting_orders.append((unit, order))
        return conflicting_orders


    def calculate_local_strengths(self, conflicting_region, conflicting_orders):
        print('CONFLICTING REGION:', conflicting_region)
        print('  CONFLICTING ORDERS: ', conflicting_orders)

        local_strengths = {unit : 1 for unit, _ in conflicting_orders}

        # regions with units moving into conflicting region
        attacks_from = []
        for unit, order in conflicting_orders:
            if type(order) == Move and order.region != conflicting_region:
                attacks_from.append(order.region)
        
        return self.add_strength_from_supports(local_strengths, attacks_from, \
                                          conflicting_region, conflicting_orders)


    def add_strength_from_supports(self, local_strengths, attacks_from, \
                                conflicting_region, conflicting_orders):
        for unit, order in conflicting_orders:
            if type(order) == Support:
                supported_region = order.from_

                # check if support has been cut
                if supported_region:
                    supported_unit = self.get_unit_by_region(supported_region)
                    if supported_unit in local_strengths.keys():
                        # case when order is supporting the conflicting region
                        if order.to == conflicting_region:
                            local_strengths[supported_unit] += 1

                        # case when units attacking each other
                        elif order.to in attacks_from:
                            local_strengths[supported_unit] += 1
        return local_strengths
        

    def get_supporting_regions(self, region):
        supporting_regions = []
        for unit, order in self.moves.items():
            if type(order) == Support and order.from_ == region:
                supporting_regions.append(order.region)
        return supporting_regions


    def get_supporting_orders(self, region):
        supporting_orders = []
        for unit, order in self.moves.items():
            if type(order) == Support and order.from_ == region:
                supporting_orders.append(order)
        return supporting_orders


    def get_supported_unit(self, unit):
        from_ = self.moves[unit].from_
        to = self.moves[unit].to
        for unit, order in self.moves.items():
            if order.region == from_ and order.to == to or \
               order.region == from_ and type(order) == Hold:
                return unit


    def update_regions(self):
        self.clear_all_regions()
        for unit, region in self.results.items():
            self.regions[region].unit = unit


    def clear_all_regions(self):
        for region in self.regions.values():
            region.unit = None
        

    def create_unit(self, order):
        # bring back these checks near end
        #if self.regions[order.region].supply == True and \
        #self.regions[order.region].unit == None and \
        #self.regions[order.region].owner == order.player:
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


    def print_extended_board(self):
        print('----------------------------------')
        print('|  Clyde   |   Edin   |  Nwg Sea |')
        print('|          |', end = '') if not self.regions['Clyde'].unit \
        else print('|    A     |', end = '')
        print('          |', end = '') if not self.regions['Edinburgh'].unit \
        else print('    A     |', end = '')
        print('          |') if not self.regions['Norwegian Sea'].unit \
        else print('     A    |')
        print('----------------------------------')
        print('| Yorkshire| Liverpool|  Nth Sea |')
        print('|          |', end = '') if not self.regions['Yorkshire'].unit \
        else print('|    A     |', end = '')
        print('          |', end = '') if not self.regions['Liverpool'].unit \
        else print('    A     |', end = '')
        print('          |') if not self.regions['North Sea'].unit \
        else print('     A    |')
        print('----------------------------------')
