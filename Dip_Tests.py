from Dip_Player import Player
from Dip_Env import Env
from Dip_Orders import Order, Create_Unit, Hold, Move, Support


def test_create_units(game, nb_units=2):
    print('-----create units test-----')
    order1 = Create_Unit(0, 'Edinburgh')
    order2 = Create_Unit(1, 'Liverpool')
    
    game.players[0].orders.append(order1)
    game.players[1].orders.append(order2)
    if nb_units == 3:
        order3 = Create_Unit(0, 'Clyde')
        game.players[0].orders.append(order3)

    game.collect_build_orders()
    print([order.details() for order in game.order_sheet])

    game.game_map.resolve_builds(game.order_sheet)
    game.board

    game.collect_results()
    
    game.game_map.reset_results()
    print()
    

def test_move_units_1(game):
    test_create_units(game)
    print('-----MOVE UNITS TEST 1-----')
    
    unit1 = game.players[0].units[0]
    unit2 = game.players[1].units[0]
    order1 = Move(0, 'Edinburgh', to='Clyde')
    order2 = Move(1, 'Liverpool', to='Yorkshire')
    unit1.orders = order1
    unit2.orders = order2
    
    game.game_map.resolve_orders(game.players)
    game.board

    assert game.game_map.regions['Clyde'].unit == hash(unit1)
    assert game.game_map.regions['Yorkshire'].unit == hash(unit2)
    print('-----MOVE UNITS TEST 1 PASSED-----')


def test_move_units_2(game):
    test_create_units(game)
    print('-----MOVE UNITS TEST 2-----')

    unit1 = game.players[0].units[0]
    unit2 = game.players[1].units[0]
    order1 = Move(0, 'Edinburgh', to='Liverpool')
    order2 = Hold(1, 'Liverpool')
    unit1.orders = order1
    unit2.orders = order2

    game.game_map.resolve_orders(game.players)
    game.board

    assert game.game_map.regions['Edinburgh'].unit == hash(unit1)
    assert game.game_map.regions['Liverpool'].unit == hash(unit2)
    print('-----MOVE UNITS TEST 2 PASSED-----')


def test_move_units_3(game):
    test_create_units(game)
    print('-----MOVE UNITS TEST 3-----')
    
    unit1 = game.players[0].units[0]
    unit2 = game.players[1].units[0]
    order1 = Move(0, 'Edinburgh', to='Liverpool')
    order2 = Move(1, 'Liverpool', to='Yorkshire')
    unit1.orders = order1
    unit2.orders = order2

    game.game_map.resolve_orders(game.players)
    game.board

    assert game.game_map.regions['Liverpool'].unit == hash(unit1)
    assert game.game_map.regions['Yorkshire'].unit == hash(unit2)
    print('-----MOVE UNITS TEST 3 PASSED-----')


def test_move_units_4(game):
    test_create_units(game)
    print('-----MOVE UNITS TEST 4-----')

    unit1 = game.players[0].units[0]
    unit2 = game.players[1].units[0]
    order1 = Move(0, 'Edinburgh', to='Yorkshire')
    order2 = Move(1, 'Liverpool', to='Yorkshire')
    unit1.orders = order1
    unit2.orders = order2

    game.game_map.resolve_orders(game.players)
    game.board

    assert game.game_map.regions['Edinburgh'].unit == hash(unit1)
    assert game.game_map.regions['Liverpool'].unit == hash(unit2)
    print('-----MOVE UNITS TEST 4 PASSED-----')


def test_move_units_5(game):
    test_create_units(game, 3)
    print('-----MOVE UNITS TEST 5-----')

    unit1 = game.players[0].units[0]
    unit2 = game.players[1].units[0]
    unit3 = game.players[0].units[1]
    order1 = Move(0, 'Edinburgh', to='Liverpool')
    order2 = Move(1, 'Liverpool', to='Yorkshire')
    order3 = Move(0, 'Clyde', to='Yorkshire')
    unit1.orders = order1
    unit2.orders = order2
    unit3.orders = order3

    game.game_map.resolve_orders(game.players)
    game.board

    assert game.game_map.regions['Edinburgh'].unit == hash(unit1)
    assert game.game_map.regions['Liverpool'].unit == hash(unit2)
    assert game.game_map.regions['Clyde'].unit == hash(unit3)
    print('-----MOVE UNITS TEST 5 PASSED-----')
    

def test_hold_units(game):
    test_create_units(game, 2)
    print('-----HOLD UNITS TEST 1-----')

    unit1 = game.players[0].units[0]
    unit2 = game.players[1].units[0]
    order1 = Hold(0, 'Edinburgh')
    order2 = Hold(1, 'Liverpool')
    unit1.orders = order1
    unit2.orders = order2

    game.game_map.resolve_orders(game.players)
    game.board

    assert game.game_map.regions['Edinburgh'].unit == hash(unit1)
    assert game.game_map.regions['Liverpool'].unit == hash(unit2)
    print('-----HOLD UNITS TEST 1 PASSED-----')


def test_support_1(game):
    test_create_units(game, 3)
    print('-----SUPPORT UNITS TEST 1-----')

    unit1 = game.players[0].units[0]
    unit2 = game.players[1].units[0]
    unit3 = game.players[0].units[1]
    order1 = Move(0, 'Edinburgh', to='Yorkshire')
    order2 = Move(1, 'Liverpool', to='Yorkshire')
    order3 = Support(0, 'Clyde', from_='Edinburgh', to='Yorkshire')
    unit1.orders = order1
    unit2.orders = order2
    unit3.orders = order3

    game.game_map.resolve_orders(game.players)
    game.board

    assert game.game_map.regions['Yorkshire'].unit == hash(unit1)
    assert game.game_map.regions['Liverpool'].unit == hash(unit2)
    assert game.game_map.regions['Clyde'].unit == hash(unit3)
    print('-----SUPPORT UNITS TEST 1 PASSED-----')


def test_support_2(game):
    test_create_units(game, 3)
    print('-----SUPPORT UNITS TEST 2-----')

    unit1 = game.players[0].units[0]
    unit2 = game.players[1].units[0]
    unit3 = game.players[0].units[1]
    order1 = Support(0, 'Edinburgh', from_='Clyde', to='Yorkshire')
    order2 = Move(1, 'Liverpool', to='Edinburgh')
    order3 = Move(0, 'Clyde', to='Yorkshire')
    unit1.orders = order1
    unit2.orders = order2
    unit3.orders = order3

    game.game_map.resolve_orders(game.players)
    game.board

    assert game.game_map.regions['Edinburgh'].unit == hash(unit1)
    assert game.game_map.regions['Liverpool'].unit == hash(unit2)
    assert game.game_map.regions['Yorkshire'].unit == hash(unit3)

    strengths = ([strength for strength in game.game_map.strengths.values()])
    assert strengths == [1, 1, 1]

    
    print('-----SUPPORT UNITS TEST 2 PASSED-----')


def test_support_3(game):
    test_create_units(game, 3)
    print('-----SUPPORT UNITS TEST 3-----')

    unit1 = game.players[0].units[0]
    unit2 = game.players[1].units[0]
    unit3 = game.players[0].units[1]
    order1 = Move(0, 'Edinburgh', to='Liverpool')
    order2 = Hold(1, 'Liverpool')
    order3 = Support(0, 'Clyde', from_='Edinburgh', to='Liverpool')
    unit1.orders = order1
    unit2.orders = order2
    unit3.orders = order3

    game.game_map.resolve_orders(game.players)
    game.board

    assert game.game_map.regions['Edinburgh'].unit == hash(unit1)
    assert game.game_map.regions['Liverpool'].unit == hash(unit2)
    assert game.game_map.regions['Yorkshire'].unit == hash(unit3)

    strengths = ([strength for strength in game.game_map.strengths.values()])
    assert strengths == [1, 1, 1]

    
    print('-----SUPPORT UNITS TEST 3 PASSED-----')
