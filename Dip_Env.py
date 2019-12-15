from Dip_Player import Player, Move_Order, Army
from collections import OrderedDict, namedtuple




class Game:
    def __init__(self):
        self.order_sheet = None
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

    #def collect_orders(self):


class Env:
    def __init__(self):
        self.regions = OrderedDict([
            ('Clyde', Region(owner=None, supply=False, army=None, water=False, coastal=True, home=None,
                             neighbours=['Edinburgh', 'Liverpool', 'Yorkshire'])),
            ('Edinburgh', Region(owner=0, supply=True, army=None, water=False, coastal=True, home=0,
                             neighbours=['Clyde', 'Liverpool', 'Yorkshire'])),
            ('Yorkshire', Region(owner=None, supply=False, army=None, water=False, coastal=True, home=None,
                             neighbours=['Clyde', 'Edinburgh', 'Liverpool'])),
            ('Liverpool', Region(owner=0, supply=True, army=None, water=False, coastal=True, home=0,
                             neighbours=['Clyde', 'Edinburgh', 'Yorkshire']))
            ])

    def lodge_move(self, from_, to, owner):
        print(self.regions[from_].army.owner)
        print(owner)
        #if self.regions[from_].army.owner = owner:

    def move_army(move_arg):
        if type(move_arg) == Move_Order:
            print('Can move')

    def create_army(self, owner, type_, region):
        if not self.regions[region].army and self.regions[region].supply:
            if type_ == 'army':
                self.regions[region].army = Army(owner, False, region) 
            else:
                self.regions[region].army = Army(owner, True, region)

    def print_board(self):
        print('-----------------------')
        print('|  Clyde   |   Edin   |')
        print('|          |', end = '') if not self.regions['Clyde'].army \
        else print('|    A     |', end = '')
        print('          |') if not self.regions['Edinburgh'].army \
        else print('    A     |')
        print('-----------------------')
        print('| Yorkshire| Liverpool|')
        print('|          |', end = '') if not self.regions['Yorkshire'].army \
        else print('|    A     |', end = '')
        print('          |') if not self.regions['Liverpool'].army \
        else print('    A     |')
        print('-----------------------')



if __name__ == '__main__':
    game = Game()
    game.initiate()
    game.initiate_prints()
    
    ##game_map.create_army(1, 'army', 'Edinburgh')
        

    Move1 = Move_Order('Edin', 1).details('Edin', 'Yorkshire')




