from Dip_Player import Player
from Dip_Env import Env


class Game:
    def __init__(self):
        self.order_sheet = []
        self.phase = 0
        self.phases = ['orders', 'retreat', 'orders', 'retreat', 'build']
        self.players = []
        self.game_map = Env()


    def initiate(self):
        names = ['Charles', 'Sam']
        for i in range(2):
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

    #def collect_orders(self):


if __name__ == '__main__':
    game = Game()
    game.initiate()
    game.initiate_prints()
    print()
    print(f'Phase: {game.get_phase}')
    print(game.players)
    game.board

