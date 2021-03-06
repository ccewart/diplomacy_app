import io
import sys

from Env import Env
from Player import Player
from Tests import *


class Game:
    def __init__(self, nb_players):
        self.order_sheet = []
        self.phase = 0
        self.phases = ["orders", "retreat", "orders", "retreat", "build"]
        self.players = []
        self.game_map = Env(nb_players)
        self.nb_players = nb_players
        names = ["Charles", "Sam"]
        for i in range(self.nb_players):
            self.players.append(Player(names[i], i))

    def reset_order_sheet(self):
        self.order_sheet = []
        for player in self.players:
            player.orders = []

    def initiate_prints(self):
        print("INITIATING GAME")
        for player in self.players:
            print("Name: ", player.name, "\t", "Faction: ", player.faction)
        self.game_map.print_board()

    def next_phase(self):
        self.phase += 1
        self.phase = self.phase % 5

    @property
    def get_phase(self):
        return self.phases[self.phase]

    def print_board(self):
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

    def function():
        disable_prints()
        wrapped_game = Game(2)
        try:
            func(wrapped_game)
            enable_prints()
            print(func.__name__, ": passed")
        except Exception:
            enable_prints()
            print(func.__name__, ": failed")

    return function


def run_all_tests():
    decorated_test_hold_units = test_wrapper(test_hold_units)
    decorated_test_move_units_1 = test_wrapper(test_move_units_1)
    decorated_test_move_units_2 = test_wrapper(test_move_units_2)
    decorated_test_move_units_3 = test_wrapper(test_move_units_3)
    decorated_test_move_units_4 = test_wrapper(test_move_units_4)
    decorated_test_move_units_5 = test_wrapper(test_move_units_5)
    decorated_test_move_units_6 = test_wrapper(test_move_units_6)
    decorated_test_move_units_7 = test_wrapper(test_move_units_7)
    decorated_test_support_1 = test_wrapper(test_support_1)
    decorated_test_support_2 = test_wrapper(test_support_2)
    decorated_test_support_3 = test_wrapper(test_support_3)
    decorated_test_support_4 = test_wrapper(test_support_4)
    decorated_test_support_5 = test_wrapper(test_support_5)
    decorated_test_support_6 = test_wrapper(test_support_6)
    decorated_test_support_7 = test_wrapper(test_support_7)
    decorated_test_support_8 = test_wrapper(test_support_8)
    decorated_test_support_9 = test_wrapper(test_support_9)
    decorated_test_support_10 = test_wrapper(test_support_10)
    decorated_test_support_11 = test_wrapper(test_support_11)
    decorated_test_support_12 = test_wrapper(test_support_12)
    decorated_test_support_13 = test_wrapper(test_support_13)

    decorated_test_hold_units()
    decorated_test_move_units_1()
    decorated_test_move_units_2()
    decorated_test_move_units_3()
    decorated_test_move_units_4()
    decorated_test_move_units_5()
    decorated_test_move_units_6()
    decorated_test_move_units_7()
    decorated_test_support_1()
    decorated_test_support_2()
    decorated_test_support_3()
    decorated_test_support_4()
    decorated_test_support_5()
    decorated_test_support_6()
    decorated_test_support_7()
    decorated_test_support_8()
    decorated_test_support_9()
    decorated_test_support_10()
    decorated_test_support_11()
    decorated_test_support_12()
    decorated_test_support_13()


if __name__ == '__main__':
    game = Game(2)
    # game.initiate_prints()
    # game.reset_order_sheet()

    run_all_tests()

    # test_hold_units(game)
    # test_move_units_1(game)
    # test_move_units_2(game)
    # test_move_units_3(game)
    # test_move_units_4(game)
    # test_move_units_5(game)
    # test_move_units_6(game)
    # test_move_units_7(game)
    # test_support_1(game)
    # test_support_2(game)
    # test_support_3(game)
    # test_support_4(game)
    # test_support_5(game)
    # test_support_6(game)
    # test_support_7(game)
    # test_support_8(game)
    # test_support_9(game)
    # test_support_10(game)
    # test_support_11(game)
    # test_support_12(game)
    # test_support_13(game)
