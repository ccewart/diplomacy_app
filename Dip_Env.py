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
        print('DISLODGED:', self.dislodged)
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
        #print('MOVES:', self.moves)
        print('CONFLICTS:', conflicts)
        conflicting_region = conflicts.pop()
        conflicting_orders = self.get_conflicting_orders(conflicting_region)

        local_strengths = self.calculate_local_strengths(conflicting_region,\
                                                         conflicting_orders)
        strongest_orders = [item for item in local_strengths.items() if \
                            item[1] == max(local_strengths.values())]

        print('LOCAL STRENGTHS:', local_strengths)
        print('CONFLICTING REGION:', conflicting_region)
        print('CONFLICTING ORDERS: ', conflicting_orders)
        print('STRONGEST_ORDERS:', strongest_orders)

        # unoccupied space, strongest move wont bounce
        if len(strongest_orders) == 1:
            strongest_unit = strongest_orders[0][0]
            self.moves[strongest_unit].resolved = True
        
        # occupied space, strongest move wont bounce, unit dislodged
        if len(strongest_orders) == 1 and self.regions[conflicting_region].unit:
            strongest_unit = strongest_orders[0][0]
            dislodged_unit = hash(self.regions[conflicting_region].unit)
            self.moves[strongest_unit].resolved = True
            dislodged_moves = self.moves.pop(dislodged_unit)
            self.dislodged[dislodged_unit] = dislodged_moves
            conflicting_orders = [item for item in conflicting_orders if item[0]\
                                  not in [key for key in self.dislodged.keys()]]

        # bounce unsuccessful move orders
        for unit, order in conflicting_orders:
            if type(order) == Move and order.resolved == False:
                self.moves[unit].to = self.moves[unit].region
        
        print()
        return self.find_conflicts()


    def get_conflicting_orders(self, conflicting_region):
        conflicting_orders = []
        for unit, order in self.moves.items():
            if order.to == conflicting_region or \
            order.region == conflicting_region:
                conflicting_orders.append((unit, order))
        return conflicting_orders


    def calculate_local_strengths(self, conflicting_region, conflicting_orders):
        local_strengths = {}
        print('CONFLICTING ORDERS:', conflicting_orders)
        for unit, _ in conflicting_orders:
            local_strengths[unit] = 1
        for unit, order in conflicting_orders:

            # case when support order is the conflicting region
            if type(order) == Support and order.region == conflicting_region:
                print('----CASE 1----')
                pass

            # case when order is supporting the conflicting region
            if type(order) == Support and order.to == conflicting_region:
                print('----CASE 2----')
                region = order.from_
                print('region:', region)
                supported_unit = self.get_unit_by_region(region)
                local_strengths[supported_unit] += 1

            
            if type(order) == Move and self.regions[order.to].unit:
                affected_unit = self.get_unit_by_region(order.to)
                supported_unit = self.get_supported_unit(affected_unit)
                if type(self.moves[affected_unit]) == Support:
                    local_strengths[supported_unit] -= 1
        return local_strengths
        

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
