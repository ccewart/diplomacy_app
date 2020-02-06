from Dip_Player import Player
from Dip_Env import Env
from Dip_Orders import Order, Create_Unit, Hold, Move, Support
from Dip_Tests import *

class Game:
    def __init__(self, nb_players):
        self.order_sheet = []
        self.phase = 0
        self.phases = ['orders', 'retreat', 'orders', 'retreat', 'build']
        self.players = []
        self.game_map = Env(nb_players)
        self.nb_players = nb_players


    def reset_order_sheet(self):
        self.order_sheet = []


    def initiate(self):
        names = ['Charles', 'Sam']
        for i in range(self.nb_players):
            self.players.append(Player(names[i], i))


    def initiate_prints(self):
        print('INITIATING GAME')
        for player in self.players:
            print('Name: ', player.name,'\t', 'Faction: ', player.faction)
        self.game_map.print_board()


    def get_unit(self, player, unit):
        return game.players[player].units[unit]
    

    def next_phase(self):
        self.phase += 1
        self.phase = self.phase % 5


    @property
    def get_phase(self):
        return self.phases[self.phase]


    @property
    def board(self):
        self.game_map.print_board()


    def collect_build_orders(self):
        for player in self.players:
            for order in player.orders:
                self.order_sheet.append(order)


    def collect_results(self):
        for unit, _, player in self.game_map.results.values():
            game.players[player].units.append(unit)
    

if __name__ == '__main__':
    game = Game(2)
    game.initiate()
    #game.initiate_prints()
    #game.reset_order_sheet()

    #test_hold_units(game)
    #test_move_units_1(game)
    #test_move_units_2(game)
    #test_move_units_3(game)
    #test_move_units_4(game)
    #test_move_units_5(game)
    #test_support_1(game)
    #test_support_2(game)
    #test_support_3(game)
    test_support_4(game)
