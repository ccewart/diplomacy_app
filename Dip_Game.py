from Dip_Player import Player
from Dip_Env import Env
from Dip_Orders import Order, Create_Unit, Hold, Move, Support
from Dip_Tests import *
import io
import sys

class Game:
    def __init__(self, nb_players):
        self.order_sheet = []
        self.phase = 0
        self.phases = ['orders', 'retreat', 'orders', 'retreat', 'build']
        self.players = []
        self.game_map = Env(nb_players)
        self.nb_players = nb_players
        names = ['Charles', 'Sam']
        for i in range(self.nb_players):
            self.players.append(Player(names[i], i))


    def reset_order_sheet(self):
        self.order_sheet = []


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
            self.players[player].units.append(unit)




def test_wrapper(func):
    old_stdout = sys.stdout
    def disable_prints():
        text_trap = io.StringIO()
        sys.stdout = text_trap

    def enable_prints():
        sys.stdout = old_stdout
    
    def function(game):
        disable_prints()
        passed = func(game)
        enable_prints()
        result = 'passed' if passed else 'failed'
        print('MOVE UNITS TEST 1:', result)
    return function


def run_all_tests():
    game = Game(2)

    decorated_test_move_units_1 = test_wrapper(test_move_units_1)
    decorated_test_move_units_2 = test_wrapper(test_move_units_2)
    decorated_test_move_units_3 = test_wrapper(test_move_units_3)
    decorated_test_move_units_4 = test_wrapper(test_move_units_4)
    decorated_test_move_units_5 = test_wrapper(test_move_units_5)
    decorated_test_support_1 = test_wrapper(test_support_1)
    decorated_test_support_2 = test_wrapper(test_support_2)
    decorated_test_support_3 = test_wrapper(test_support_3)

    decorated_test_move_units_1(game)
    decorated_test_move_units_2(game)
    decorated_test_move_units_3(game)
    decorated_test_move_units_4(game)
    decorated_test_move_units_5(game)
    decorated_test_support_1(game)
    decorated_test_support_2(game)
    decorated_test_support_3(game)


if __name__ == '__main__':
    #game = Game(2)
    #game.initiate_prints()
    #game.reset_order_sheet()

    run_all_tests()

    #test_hold_units(game)
    #test_move_units_1(game)
    #test_move_units_2(game)
    #test_move_units_3(game)
    #test_move_units_4(game)
    #test_move_units_5(game)
    #test_support_1(game)
    #test_support_2(game)
    #test_support_3(game)
    #test_support_4(game)

    
