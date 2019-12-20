from Dip_Player import Player
from Dip_Env import Env
from Dip_Orders import Order, Create_Army, Hold, Move, Support


class Game:
    def __init__(self, nb_players):
        self.order_sheet = []
        self.phase = 0
        self.phases = ['orders', 'retreat', 'orders', 'retreat', 'build']
        self.players = []
        self.game_map = Env(nb_players)
        self.nb_players = nb_players


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
            self.order_sheet.append(player.orders)


if __name__ == '__main__':
    game = Game(2)
    game.initiate()
    game.initiate_prints()
    print()
    print(f'Phase: {game.get_phase}')

    # Player 0 create army
    order1 = Create_Army(0, 'Edinburgh')
    game.players[0].orders.append(order1)

    # Player 1 create army
    order2 = Create_Army(1, 'Liverpool')
    game.players[1].orders.append(order2)

    game.order_sheet.append(order1)
    game.order_sheet.append(order2)
    for order in game.order_sheet:
        print(order.details())

    game.game_map.submit_orders(game.order_sheet)
    game.board
    print()
    
    # new order sheet
    game.order_sheet = []
    # Player 0 moves army
    order3 = Move(0, 'Edinburgh', to='Clyde')
    # Player 1 moves army
    order4 = Move(1, 'Liverpool', to='Yorkshire')

    game.order_sheet.append(order3)
    game.order_sheet.append(order4)

    game.game_map.submit_orders(game.order_sheet)

    game.board
    
    game.game_map.resolve_orders()
