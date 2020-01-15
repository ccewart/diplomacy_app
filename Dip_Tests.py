from Dip_Player import Player
from Dip_Env import Env
from Dip_Orders import Order, Create_Unit, Hold, Move, Support


def test_create_units(game):
    print('-----create units test-----')
    order1 = Create_Unit(0, 'Edinburgh')
    order2 = Create_Unit(1, 'Liverpool')
    game.players[0].orders.append(order1)
    game.players[1].orders.append(order2)

    game.collect_orders()
    print([order.details() for order in game.order_sheet])

    game.game_map.submit_orders(game.order_sheet)
    game.board


def test_move_units(game):
    print('-----move units test-----')
    order3 = Move(0, 'Edinburgh', to='Clyde')
    order4 = Move(1, 'Liverpool', to='Yorkshire')
    game.order_sheet.append(order3)
    game.order_sheet.append(order4)

    game.game_map.submit_orders(game.order_sheet)
    game.game_map.resolve_orders()
    print('game.moves:', game.game_map.moves)
    print()
    game.board
