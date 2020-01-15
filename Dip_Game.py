from Dip_Player import Player
from Dip_Env import Env
from Dip_Orders import Order, Create_Unit, Hold, Move, Support
from Dip_Tests import test_create_units, test_move_units


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


    def next_phase(self):
        self.phase += 1
        self.phase = self.phase % 5


    @property
    def get_phase(self):
        return self.phases[self.phase]


    @property
    def board(self):
        self.game_map.print_board()


    def collect_orders(self):
        for player in self.players:
            for order in player.orders:
                self.order_sheet.append(order)


if __name__ == '__main__':
    game = Game(2)
    game.initiate()
    game.initiate_prints()
    print()
    
    test_create_units(game)

    print(f'\nPhase: {game.get_phase}\n')
    
    game.reset_order_sheet()

    test_move_units(game)

