from Dip_Player import Player
from Dip_Env import Env
from Dip_Orders import Order, Create_Unit, Hold, Move, Support


def test_create_units(game):
    print('-----create units test-----')
    order1 = Create_Unit(0, 'Edinburgh')
    order2 = Create_Unit(1, 'Liverpool')
    game.players[0].orders.append(order1)
    game.players[1].orders.append(order2)

    game.collect_build_orders()
    print([order.details() for order in game.order_sheet])

    game.game_map.resolve_builds(game.order_sheet)
    game.board

    game.collect_results()
    
    for player in game.players:
        print(player.units)
    game.game_map.reset_results()


def test_move_units(game):
    print('-----move units test-----')
    order3 = Move(0, 'Edinburgh', to='Clyde')
    order4 = Move(1, 'Liverpool', to='Yorkshire')
    game.players[0].units[0].orders = order3
    game.players[1].units[0].orders = order4

    game.game_map.resolve_orders(game.players)
    print('game.game_map.moves:', game.game_map.moves)
    print('game.game_map.units:', game.game_map.units)
    print('game.game_map.results:', game.game_map.results)
    print()
    game.board


def test_move_units_2(game):
    print('-----move units test-----')
    order3 = Move(0, 'Edinburgh', to='Yorkshire')
    order4 = Move(1, 'Liverpool', to='Yorkshire')
    game.players[0].units[0].orders = order3
    game.players[1].units[0].orders = order4

    game.game_map.resolve_orders(game.players)
    print('game.game_map.moves:', game.game_map.moves)
    #print('game.game_map.units:', game.game_map.units)
    print('game.game_map.results:', game.game_map.results)
    print()
    game.board







