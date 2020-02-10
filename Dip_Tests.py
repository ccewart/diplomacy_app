from Dip_Player import Player
from Dip_Env import Env
from Dip_Orders import Order, Create_Unit, Hold, Move, Support


def test_create_units(game, build_orders):
    for player, region in build_orders:
        order = Create_Unit(player, region)
        game.players[player].orders.append(order)

    game.collect_build_orders()
    print([order.details() for order in game.order_sheet])

    game.game_map.resolve_builds(game.order_sheet)
    game.board
    
    game.collect_results()
    
    game.game_map.reset_results()
    print()


def test_move_units_1(game):
    move_1_units = [(0, 'Edinburgh'), (1, 'Liverpool')]
    test_create_units(game, move_1_units)
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
    assert game.game_map.regions['Edinburgh'].unit == None
    assert game.game_map.regions['Yorkshire'].unit == hash(unit2)
    assert game.game_map.regions['Liverpool'].unit == None
    print('-----MOVE UNITS TEST 1 PASSED-----')


def test_move_units_2(game):
    move_2_units = [(0, 'Edinburgh'), (1, 'Liverpool')]
    test_create_units(game, move_2_units)
    print('-----MOVE UNITS TEST 2-----')

    unit1 = game.players[0].units[0]
    unit2 = game.players[1].units[0]
    order1 = Move(0, 'Edinburgh', to='Liverpool')
    order2 = Hold(1, 'Liverpool')
    unit1.orders = order1
    unit2.orders = order2

    game.game_map.resolve_orders(game.players)
    game.board

    assert game.game_map.regions['Clyde'].unit == None
    assert game.game_map.regions['Edinburgh'].unit == hash(unit1)
    assert game.game_map.regions['Yorkshire'].unit == None
    assert game.game_map.regions['Liverpool'].unit == hash(unit2)
    print('-----MOVE UNITS TEST 2 PASSED-----')


def test_move_units_3(game):
    move_3_units = [(0, 'Edinburgh'), (1, 'Liverpool')]
    test_create_units(game, move_3_units)
    print('-----MOVE UNITS TEST 3-----')
    
    unit1 = game.players[0].units[0]
    unit2 = game.players[1].units[0]
    order1 = Move(0, 'Edinburgh', to='Liverpool')
    order2 = Move(1, 'Liverpool', to='Yorkshire')
    unit1.orders = order1
    unit2.orders = order2

    game.game_map.resolve_orders(game.players)
    game.board

    assert game.game_map.regions['Clyde'].unit == None
    assert game.game_map.regions['Edinburgh'].unit == None
    assert game.game_map.regions['Yorkshire'].unit == hash(unit2)
    assert game.game_map.regions['Liverpool'].unit == hash(unit1)
    
    print('-----MOVE UNITS TEST 3 PASSED-----')


def test_move_units_4(game):
    move_4_units = [(0, 'Edinburgh'), (1, 'Liverpool')]
    test_create_units(game, move_4_units)
    print('-----MOVE UNITS TEST 4-----')

    unit1 = game.players[0].units[0]
    unit2 = game.players[1].units[0]
    order1 = Move(0, 'Edinburgh', to='Yorkshire')
    order2 = Move(1, 'Liverpool', to='Yorkshire')
    unit1.orders = order1
    unit2.orders = order2

    game.game_map.resolve_orders(game.players)
    game.board

    assert game.game_map.regions['Clyde'].unit == None
    assert game.game_map.regions['Edinburgh'].unit == hash(unit1)
    assert game.game_map.regions['Yorkshire'].unit == None
    assert game.game_map.regions['Liverpool'].unit == hash(unit2)
    print('-----MOVE UNITS TEST 4 PASSED-----')


def test_move_units_5(game):
    move_5_units = [(0, 'Edinburgh'), (0, 'Clyde'), (1, 'Liverpool')]
    test_create_units(game, move_5_units)
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

    assert game.game_map.regions['Clyde'].unit == hash(unit3)
    assert game.game_map.regions['Edinburgh'].unit == hash(unit1)
    assert game.game_map.regions['Yorkshire'].unit == None
    assert game.game_map.regions['Liverpool'].unit == hash(unit2)
    
    print('-----MOVE UNITS TEST 5 PASSED-----')


def test_move_units_6(game):
    move_6_units = [(0, 'Edinburgh'), (1, 'Liverpool')]
    test_create_units(game, move_6_units)
    print('-----MOVE UNITS TEST 6-----')

    unit1 = game.players[0].units[0]
    unit2 = game.players[1].units[0]
    print(hash(unit1))
    print(hash(unit2))
    order1 = Move(0, 'Edinburgh', to='Liverpool')
    order2 = Move(1, 'Liverpool', to='Edinburgh')
    unit1.orders = order1
    unit2.orders = order2

    game.game_map.resolve_orders(game.players)
    game.board

    assert game.game_map.regions['Clyde'].unit == None
    assert game.game_map.regions['Edinburgh'].unit == hash(unit1)
    assert game.game_map.regions['Yorkshire'].unit == None
    assert game.game_map.regions['Liverpool'].unit == hash(unit2)
    
    print('-----MOVE UNITS TEST 6 PASSED-----')
    

def test_hold_units(game):
    hold_units = [(0, 'Edinburgh'), (1, 'Liverpool')]
    test_create_units(game, hold_units)
    print('-----HOLD UNITS TEST 1-----')

    unit1 = game.players[0].units[0]
    unit2 = game.players[1].units[0]
    order1 = Hold(0, 'Edinburgh')
    order2 = Hold(1, 'Liverpool')
    unit1.orders = order1
    unit2.orders = order2

    game.game_map.resolve_orders(game.players)
    game.board

    assert game.game_map.regions['Clyde'].unit == None
    assert game.game_map.regions['Edinburgh'].unit == hash(unit1)
    assert game.game_map.regions['Yorkshire'].unit == None
    assert game.game_map.regions['Liverpool'].unit == hash(unit2)
    print('-----HOLD UNITS TEST 1 PASSED-----')


def test_support_1(game):
    support_1_units = [(0, 'Edinburgh'), (0, 'Clyde'), (1, 'Liverpool')]
    test_create_units(game, support_1_units)
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

    assert game.game_map.regions['Clyde'].unit == hash(unit3)
    assert game.game_map.regions['Edinburgh'].unit == None
    assert game.game_map.regions['Yorkshire'].unit == hash(unit1)
    assert game.game_map.regions['Liverpool'].unit == hash(unit2)
    
    print('-----SUPPORT UNITS TEST 1 PASSED-----')


def test_support_2(game):
    support_2_units = [(0, 'Edinburgh'), (0, 'Clyde'), (1, 'Liverpool')]
    test_create_units(game, support_2_units)
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

    assert game.game_map.regions['Clyde'].unit == None
    assert game.game_map.regions['Edinburgh'].unit == hash(unit1)
    assert game.game_map.regions['Yorkshire'].unit == hash(unit3)
    assert game.game_map.regions['Liverpool'].unit == hash(unit2)

    print('-----SUPPORT UNITS TEST 2 PASSED-----')


def test_support_3(game):
    support_3_units = [(0, 'Edinburgh'), (0, 'Clyde'), (1, 'Liverpool')]
    test_create_units(game, support_3_units)
    print('-----SUPPORT UNITS TEST 3-----')

    unit1 = game.players[0].units[0]
    unit2 = game.players[1].units[0]
    unit3 = game.players[0].units[1]
    order1 = Move(0, 'Edinburgh', to='Yorkshire')
    order2 = Move(1, 'Liverpool', to='Edinburgh')
    order3 = Support(0, 'Clyde', from_='Edinburgh', to='Yorkshire')
    unit1.orders = order1
    unit2.orders = order2
    unit3.orders = order3

    game.game_map.resolve_orders(game.players)
    game.board

    assert game.game_map.regions['Clyde'].unit == hash(unit3)
    assert game.game_map.regions['Edinburgh'].unit == hash(unit2)
    assert game.game_map.regions['Yorkshire'].unit == hash(unit1)
    assert game.game_map.regions['Liverpool'].unit == None
    
    print('-----SUPPORT UNITS TEST 3 PASSED-----')


def test_support_4(game):
    support_4_units = [(0, 'Edinburgh'), (0, 'Clyde'), (1, 'Liverpool')]
    test_create_units(game, support_4_units)
    print('-----SUPPORT UNITS TEST 4-----')

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

    assert game.game_map.regions['Clyde'].unit == hash(unit3)
    assert game.game_map.regions['Edinburgh'].unit == None
    assert game.game_map.regions['Yorkshire'].unit == None
    assert game.game_map.regions['Liverpool'].unit == hash(unit1)

    assert [key for key in game.game_map.dislodged.keys()][0] == hash(unit2)

    print('-----SUPPORT UNITS TEST 4 PASSED-----')


def test_support_5(game):
    support_5_units = [(0, 'Edinburgh'), (0, 'Clyde'), (1, 'Liverpool'),\
                       (1, 'Yorkshire'), (1, 'Norwegian Sea'), (1, 'North Sea')]
    test_create_units(game, support_5_units)
    print('-----SUPPORT UNITS TEST 5-----')

    unit1 = game.players[0].units[0]  # Edin
    unit2 = game.players[0].units[1]  # Clyde
    unit3 = game.players[1].units[0]  # Liverpool
    unit4 = game.players[1].units[1]  # Yorkshire
    unit5 = game.players[1].units[2]  # Norwegian Sea
    unit6 = game.players[1].units[3]  # North Sea
    order1 = Move(0, 'Edinburgh', to='Yorkshire')
    order2 = Support(0, 'Clyde', from_='Edinburgh', to='Yorkshire')
    order3 = Support(1, 'Liverpool', from_='Yorkshire', to='Yorkshire')
    order4 = Hold(1, 'Yorkshire')
    order5 = Move(1, 'Norwegian Sea', to='Edinburgh')
    order6 = Support(1, 'North Sea', from_= 'Norwegian Sea', to='Edinburgh') 
    unit1.orders = order1
    unit2.orders = order2
    unit3.orders = order3
    unit4.orders = order4
    unit5.orders = order5
    unit6.orders = order6

    game.game_map.resolve_orders(game.players)
    game.game_map.print_extended_board()

    assert game.game_map.regions['Clyde'].unit == hash(unit2)
    assert game.game_map.regions['Edinburgh'].unit == hash(unit5)
    assert game.game_map.regions['Yorkshire'].unit == hash(unit4)
    assert game.game_map.regions['Liverpool'].unit == hash(unit3)
    assert game.game_map.regions['Norwegian Sea'].unit == None
    assert game.game_map.regions['North Sea'].unit == hash(unit6)

    assert [key for key in game.game_map.dislodged.keys()][0] == hash(unit1)


    print('-----SUPPORT UNITS TEST 5 PASSED-----')


def test_support_6(game):
    support_6_units = [(0, 'Edinburgh'), (0, 'Clyde'), (1, 'Yorkshire'), \
                   (1, 'Norwegian Sea'), (1, 'North Sea')]
    test_create_units(game, support_6_units)
    print('-----SUPPORT UNITS TEST 6-----')

    unit1 = game.players[0].units[0]  # Edin
    unit2 = game.players[0].units[1]  # Clyde
    unit3 = game.players[1].units[0]  # Yorkshire
    unit4 = game.players[1].units[1]  # Norwegian Sea
    unit5 = game.players[1].units[2]  # North Sea
    order1 = Hold(0, 'Edinburgh')
    order2 = Support(0, 'Clyde', from_='Edinburgh', to='Edinburgh')
    order3 = Move(1, 'Yorkshire', to='Clyde')
    order4 = Move(1, 'Norwegian Sea', to='Edinburgh')
    order5 = Support(1, 'North Sea', from_= 'Norwegian Sea', to='Edinburgh') 
    unit1.orders = order1
    unit2.orders = order2
    unit3.orders = order3
    unit4.orders = order4
    unit5.orders = order5

    game.game_map.resolve_orders(game.players)
    game.game_map.print_extended_board()

    assert game.game_map.regions['Clyde'].unit == hash(unit2)
    assert game.game_map.regions['Edinburgh'].unit == hash(unit4)
    assert game.game_map.regions['Yorkshire'].unit == hash(unit3)
    assert game.game_map.regions['Liverpool'].unit == None
    assert game.game_map.regions['Norwegian Sea'].unit == None
    assert game.game_map.regions['North Sea'].unit == hash(unit5)

    assert [key for key in game.game_map.dislodged.keys()][0] == hash(unit1)

    print('-----SUPPORT UNITS TEST 6 PASSED-----')


def test_support_7(game):
    support_7_units = [(0, 'Edinburgh'), (0, 'Clyde'), (1, 'Liverpool'), \
                   (1, 'Yorkshire')]
    test_create_units(game, support_7_units)
    print('-----SUPPORT UNITS TEST 7-----')

    unit1 = game.players[0].units[0]  # Edin
    unit2 = game.players[0].units[1]  # Clyde
    unit3 = game.players[1].units[0]  # Liverpool
    unit4 = game.players[1].units[1]  # Yorkshire
    order1 = Hold(0, 'Edinburgh')
    order2 = Support(0, 'Clyde', from_='Edinburgh', to='Edinburgh')
    order3 = Support(1, 'Liverpool', from_='Yorkshire', to='Clyde')
    order4 = Move(1, 'Yorkshire', to='Clyde')
    unit1.orders = order1
    unit2.orders = order2
    unit3.orders = order3
    unit4.orders = order4

    game.game_map.resolve_orders(game.players)
    game.board

    assert game.game_map.regions['Clyde'].unit == hash(unit4)
    assert game.game_map.regions['Edinburgh'].unit == hash(unit1)
    assert game.game_map.regions['Yorkshire'].unit == None
    assert game.game_map.regions['Liverpool'].unit == hash(unit3)

    assert [key for key in game.game_map.dislodged.keys()][0] == hash(unit2)

    print('-----SUPPORT UNITS TEST 7 PASSED-----')


def test_support_8(game):
    support_8_units = [(0, 'Edinburgh'), (0, 'Clyde'), (1, 'Liverpool'), \
                   (1, 'Yorkshire')]
    test_create_units(game, support_8_units)
    print('-----SUPPORT UNITS TEST 8-----')

    unit1 = game.players[0].units[0]  # Edin
    unit2 = game.players[0].units[1]  # Clyde
    unit3 = game.players[1].units[0]  # Liverpool
    unit4 = game.players[1].units[1]  # Yorkshire
    order1 = Support(0, 'Edinburgh', from_='Clyde', to='Yorkshire')
    order2 = Move(0, 'Clyde', to='Yorkshire')
    order3 = Move(1, 'Liverpool', to='Edinburgh')
    order4 = Support(1, 'Yorkshire', from_='Liverpool', to='Edinburgh')
    unit1.orders = order1
    unit2.orders = order2
    unit3.orders = order3
    unit4.orders = order4

    game.game_map.resolve_orders(game.players)
    game.board

    assert game.game_map.regions['Clyde'].unit == hash(unit2)
    assert game.game_map.regions['Edinburgh'].unit == hash(unit1)
    assert game.game_map.regions['Yorkshire'].unit == hash(unit4)
    assert game.game_map.regions['Liverpool'].unit == hash(unit3)

    print('-----SUPPORT UNITS TEST 8 PASSED-----')


def test_support_9(game):
    support_9_units = [(0, 'Edinburgh'), (0, 'Clyde'), (1, 'Liverpool'), \
                   (1, 'Yorkshire')]
    test_create_units(game, support_9_units)
    print('-----SUPPORT UNITS TEST 9-----')

    unit1 = game.players[0].units[0]  # Edin
    unit2 = game.players[0].units[1]  # Clyde
    unit3 = game.players[1].units[0]  # Liverpool
    unit4 = game.players[1].units[1]  # Yorkshire
    print(hash(unit1))
    print(hash(unit2))
    print(hash(unit3))
    print(hash(unit4))
    order1 = Support(0, 'Edinburgh', from_='Clyde', to='Yorkshire')
    order2 = Move(0, 'Clyde', to='Yorkshire')
    order3 = Support(1, 'Liverpool', from_='Yorkshire', to='Clyde')
    order4 = Move(1, 'Yorkshire', to='Clyde')
    unit1.orders = order1
    unit2.orders = order2
    unit3.orders = order3
    unit4.orders = order4

    game.game_map.resolve_orders(game.players)
    game.board

    assert game.game_map.regions['Clyde'].unit == hash(unit2)
    assert game.game_map.regions['Edinburgh'].unit == hash(unit1)
    assert game.game_map.regions['Yorkshire'].unit == hash(unit4)
    assert game.game_map.regions['Liverpool'].unit == hash(unit3)

    print('-----SUPPORT UNITS TEST 9 PASSED-----')







