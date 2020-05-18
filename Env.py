from collections import OrderedDict
from Orders import CreateUnit, Hold, Move, Support
from Env_Classes import Region, Army, Fleet


class Env:
    def __init__(self, nb_players):
        self.orders = {}
        self.units = {}
        self.strengths = {}
        self.results = {}
        self.dislodged = {}
        self.regions = OrderedDict([
            ("Clyde", Region(name="Clyde", owner=0, supply=True,
                             unit=None, water=False, coastal=True, home=None,
                             neighbours=["Edinburgh", "Liverpool", "Yorkshire"])),
            ("Edinburgh", Region(name="Edinburgh", owner=0, supply=True,
                                 unit=None, water=False,
                                 coastal=True, home=0,
                                 neighbours=["Clyde", "Liverpool", "Yorkshire"])),
            ("Yorkshire", Region(name="Yorkshire", owner=None, supply=True,
                                 unit=None, water=False, coastal=True, home=None,
                                 neighbours=["Clyde", "Edinburgh", "Liverpool"])),
            ("Liverpool", Region(name="Liverpool", owner=1, supply=True,
                                 unit=None, water=False,
                                 coastal=True, home=0,
                                 neighbours=["Clyde", "Edinburgh", "Yorkshire"])),
            ("Norwegian Sea", Region(name="Norwegian Sea", owner=1, supply=True,
                                     unit=None, water=False,
                                     coastal=True, home=0,
                                     neighbours=["Edinburgh", "Liverpool"])),
            ("North Sea", Region(name="Liverpool", owner=1, supply=True,
                                 unit=None, water=False,
                                 coastal=True, home=0,
                                 neighbours=["Edinburgh", "Liverpool"]))
        ])

    def resolve_builds(self, order_sheet):
        """
        Create units from orders in order sheet
        :param order_sheet:
        """
        for order in order_sheet:
            if type(order) == CreateUnit:
                self.create_unit(order)

    def resolve_orders(self, players):
        """
        Find a resolution to orders and update the game map
        :param players:
        """
        self.collect_orders(players)
        self.cut_support()

        conflicts = self.find_conflicts()
        while conflicts:
            conflicts = self.resolve_conflict(conflicts)
        for unit, order in self.orders.items():
            if type(order) == Move:
                self.results[unit] = order.to
            if type(order) == Hold or type(order) == Support:
                self.results[unit] = order.region
        print("RESULTS:", self.results)
        print("DISLODGED:", self.dislodged)
        self.update_regions()

    def find_conflicts(self):
        """
        Find regions in which a conflict is taking place
        :return conflicting_regions:
        """
        conflicting_regions = []
        for unit, order in self.orders.items():
            if type(order) == Move and order.resolved == False:
                conflicting_regions.append(order.to)
                # case when units are moving into each other
                targeted_unit = self.get_unit_by_region(order.to)
                if targeted_unit:
                    if self.orders[targeted_unit].to == order.region and unit != targeted_unit:
                        conflicting_regions.append(order.to)
            if type(order) == Hold or type(order) == Support:
                conflicting_regions.append(order.region)
        return set([i for i in conflicting_regions if conflicting_regions.count(i) > 1])

    def collect_orders(self, players):
        """
        Add all units and orders to env dictionaries. Units with no orders hold by default
        :param players:
        """
        for player in players:
            for unit in player.units:
                if unit.orders is None:
                    unit.orders = Hold(player, unit.region)
                self.units[hash(unit)] = unit
                self.orders[hash(unit)] = unit.orders

    def resolve_conflict(self, conflicts):
        """
        :param conflicts:
        :return updated list of conflicts:
        """
        print("CONFLICTS:", conflicts)
        conflicting_region = conflicts.pop()
        conflicting_orders = self.get_conflicting_orders(conflicting_region)
        local_strengths = self.calculate_local_strengths(conflicting_region, conflicting_orders)
        strongest_orders = [item for item in local_strengths.items() if
                            item[1] == max(local_strengths.values())]
        print("  LOCAL STRENGTHS:", local_strengths)
        print("  STRONGEST_ORDERS:", strongest_orders)

        # unoccupied space, move successful
        if len(strongest_orders) == 1:
            strongest_unit = strongest_orders[0][0]
            self.orders[strongest_unit].resolved = True

        # unit dislodged, remove their orders from conflicting_orders
        conflicting_orders = self.resolve_dislodges(conflicting_region, conflicting_orders, strongest_orders)

        # bounce unresolved move orders
        self.resolve_unsuccessful_moves(conflicting_orders)

        return self.find_conflicts()

    def resolve_dislodges(self, conflicting_region, conflicting_orders, strongest_orders):
        """
        Update conflicting orders if a unit is dislodged. Add dislodged units to dislodged
        dictionary
        :param conflicting_region:
        :param conflicting_orders:
        :param strongest_orders:
        :return conflicting_orders:
        """
        if len(strongest_orders) == 1 and self.regions[conflicting_region].unit:
            strongest_unit = strongest_orders[0][0]
            dislodged_unit = hash(self.regions[conflicting_region].unit)
            self.orders[strongest_unit].resolved = True
            dislodged_moves = self.orders.pop(dislodged_unit)
            self.dislodged[dislodged_unit] = dislodged_moves
            conflicting_orders = [item for item in conflicting_orders if item[0]
                                  not in [key for key in self.dislodged.keys()]]
        return conflicting_orders

    def resolve_unsuccessful_moves(self, conflicting_orders):
        """
        If a move order never gets resolved, change its 'to' location to itself
        :param conflicting_orders:
        """
        for unit, order in conflicting_orders:
            if type(order) == Move and order.resolved is False:
                affected_unit = self.get_unit_by_region(order.to)
                self.orders[unit].to = self.orders[unit].region
                if affected_unit and type(self.orders[affected_unit]) == Move:
                    # case when moving into a Move order, supports update
                    supporting_orders = self.get_supporting_orders(order.region)
                    for supporting_order in supporting_orders:
                        supporting_order.to = self.orders[unit].to

    def cut_support(self):
        """
        Remove support from units which are target of a move order
        """
        for unit, order in self.orders.items():
            if type(order) == Move and self.regions[order.to].unit:
                affected_unit = self.get_unit_by_region(order.to)
                supported_unit = self.get_supported_unit(affected_unit)
                if type(self.orders[affected_unit]) == Support and supported_unit:
                    if self.orders[supported_unit].to != order.region:
                        self.orders[affected_unit].from_ = None
                        self.orders[affected_unit].to = None

    def get_conflicting_orders(self, conflicting_region):
        """
        Collect orders which are either moving to or supporting a unit moving to the
         given region
        :param conflicting_region:
        :return conflicting_orders:
        """
        conflicting_orders = []
        for unit, order in self.orders.items():
            if order.to == conflicting_region or order.region == conflicting_region:
                conflicting_orders.append((unit, order))
            elif type(order) == Support and order.from_ == conflicting_region:
                conflicting_orders.append((unit, order))
        return conflicting_orders

    def calculate_local_strengths(self, conflicting_region, conflicting_orders):
        """
        Find out who wins the conflict for a region
        :param conflicting_region:
        :param conflicting_orders:
        :return:
        """
        print("CONFLICTING REGION:", conflicting_region)
        print("  CONFLICTING ORDERS: ", conflicting_orders)

        local_strengths = {unit: 1 for unit, _ in conflicting_orders}

        # regions with units moving into conflicting region
        attacks_from = []
        for unit, order in conflicting_orders:
            if type(order) == Move and order.region != conflicting_region:
                attacks_from.append(order.region)

        return self.add_strength_from_supports(local_strengths, attacks_from, conflicting_region, conflicting_orders)

    def add_strength_from_supports(self, local_strengths, attacks_from, conflicting_region, conflicting_orders):
        """
        Modify local strengths to include extra support strength
        :param local_strengths:
        :param attacks_from:
        :param conflicting_region:
        :param conflicting_orders:
        :return local_strengths:
        """
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
        """
        Helper function. Gets all regions with units which are supporting input region
        :param region:
        :return supporting_regions:
        """
        supporting_regions = []
        for unit, order in self.orders.items():
            if type(order) == Support and order.from_ == region:
                supporting_regions.append(order.region)
        return supporting_regions

    def get_supporting_orders(self, region):
        """
        Helper function. Gets all orders which are supporting input region
        :param region:
        :return supporting_orders:
        """
        supporting_orders = []
        for unit, order in self.orders.items():
            if type(order) == Support and order.from_ == region:
                supporting_orders.append(order)
        return supporting_orders

    def get_supported_unit(self, unit):
        """
        Helper function. Gets unit which is being supported by input unit
        :param unit:
        :return supported_unit:
        """
        from_ = self.orders[unit].from_
        to = self.orders[unit].to
        for supported_unit, order in self.orders.items():
            if order.region == from_ and order.to == to or \
                    order.region == from_ and type(order) == Hold:
                return supported_unit

    def update_regions(self):
        """ Updates regions with results from last turn """
        self.clear_all_regions()
        for unit, region in self.results.items():
            self.regions[region].unit = unit

    def clear_all_regions(self):
        """ Sets all regions to have no units """
        for region in self.regions.values():
            region.unit = None

    def create_unit(self, order):
        """
        Make a new army object and place in games region dictionary
        :param order:
        """
        # bring back these checks near end:
        # if self.regions[order.region].supply == True and \
        # self.regions[order.region].unit == None and \
        # self.regions[order.region].owner == order.player:
        new_army = Army(order.player, order.region)
        self.regions[order.region].unit = new_army
        self.results[hash(new_army)] = (new_army, order.region, order.player)

    def reset_results(self):
        self.results = {}

    def get_unit_by_region(self, region):
        return hash(self.regions[region].unit) if self.regions[region].unit else None

    def print_board(self):
        print('-----------------------')
        print('|  Clyde   |   Edin   |')
        print('|          |', end='') if not self.regions['Clyde'].unit \
            else print('|    A     |', end='')
        print('          |') if not self.regions['Edinburgh'].unit \
            else print('    A     |')
        print('-----------------------')
        print('| Yorkshire| Liverpool|')
        print('|          |', end='') if not self.regions['Yorkshire'].unit \
            else print('|    A     |', end='')
        print('          |') if not self.regions['Liverpool'].unit \
            else print('    A     |')
        print('-----------------------')

    def print_extended_board(self):
        print('----------------------------------')
        print('|  Clyde   |   Edin   |  Nwg Sea |')
        print('|          |', end='') if not self.regions['Clyde'].unit \
            else print('|    A     |', end='')
        print('          |', end='') if not self.regions['Edinburgh'].unit \
            else print('    A     |', end='')
        print('          |') if not self.regions['Norwegian Sea'].unit \
            else print('     A    |')
        print('----------------------------------')
        print('| Yorkshire| Liverpool|  Nth Sea |')
        print('|          |', end='') if not self.regions['Yorkshire'].unit \
            else print('|    A     |', end='')
        print('          |', end='') if not self.regions['Liverpool'].unit \
            else print('    A     |', end='')
        print('          |') if not self.regions['North Sea'].unit \
            else print('     A    |')
        print('----------------------------------')

