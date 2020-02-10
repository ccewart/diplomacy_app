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
    elif nb_units == 5:
        game.players[1].orders.pop()
        order2 = Create_Unit(0, 'Clyde')
        order3 = Create_Unit(1, 'Yorkshire')
        game.players[1].orders.append(order3)
        order4 = Create_Unit(1, 'Norwegian Sea')
        game.players[1].orders.append(order4)
        order5 = Create_Unit(1, 'North Sea')
        game.players[1].orders.append(order5)
    elif nb_units == 6:
        order3 = Create_Unit(0, 'Clyde')
        game.players[0].orders.append(order3)
        order4 = Create_Unit(1, 'Yorkshire')
        game.players[1].orders.append(order4)
        order5 = Create_Unit(1, 'Norwegian Sea')
        game.players[1].orders.append(order5)
        order6 = Create_Unit(1, 'North Sea')
        game.players[1].orders.append(order6)

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
    assert game.game_map.regions['Edinburgh'].unit == None
    assert game.game_map.regions['Yorkshire'].unit == hash(unit2)
    assert game.game_map.regions['Liverpool'].unit == None
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

    assert game.game_map.regions['Clyde'].unit == None
    assert game.game_map.regions['Edinburgh'].unit == hash(unit1)
    assert game.game_map.regions['Yorkshire'].unit == None
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

    assert game.game_map.regions['Clyde'].unit == None
    assert game.game_map.regions['Edinburgh'].unit == None
    assert game.game_map.regions['Yorkshire'].unit == hash(unit2)
    assert game.game_map.regions['Liverpool'].unit == hash(unit1)
    
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

    assert game.game_map.regions['Clyde'].unit == None
    assert game.game_map.regions['Edinburgh'].unit == hash(unit1)
    assert game.game_map.regions['Yorkshire'].unit == None
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

    assert game.game_map.regions['Clyde'].unit == hash(unit3)
    assert game.game_map.regions['Edinburgh'].unit == hash(unit1)
    assert game.game_map.regions['Yorkshire'].unit == None
    assert game.game_map.regions['Liverpool'].unit == hash(unit2)
    
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

    assert game.game_map.regions['Clyde'].unit == None
    assert game.game_map.regions['Edinburgh'].unit == hash(unit1)
    assert game.game_map.regions['Yorkshire'].unit == None
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

    assert game.game_map.regions['Clyde'].unit == hash(unit3)
    assert game.game_map.regions['Edinburgh'].unit == None
    assert game.game_map.regions['Yorkshire'].unit == hash(unit1)
    assert game.game_map.regions['Liverpool'].unit == hash(unit2)
    
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

    assert game.game_map.regions['Clyde'].unit == None
    assert game.game_map.regions['Edinburgh'].unit == hash(unit1)
    assert game.game_map.regions['Yorkshire'].unit == hash(unit3)
    assert game.game_map.regions['Liverpool'].unit == hash(unit2)

    print('-----SUPPORT UNITS TEST 2 PASSED-----')


def test_support_3(game):
    test_create_units(game, 3)
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
    test_create_units(game, 3)
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
    test_create_units(game, 6)
    print('-----SUPPORT UNITS TEST 5-----')

    # Edin
    unit1 = game.players[0].units[0]
    print('unit1:', unit1.region)
    # Clyde
    unit2 = game.players[0].units[1]
    print('unit2:', unit2.region)
    # Liverpool
    unit3 = game.players[1].units[0]
    print('unit3:', unit3.region)
    # Yorkshire
    unit4 = game.players[1].units[1]
    print('unit4:', unit4.region)
    # Norwegian Sea
    unit5 = game.players[1].units[2]
    print('unit5:', unit5.region)
    # North Sea
    unit6 = game.players[1].units[3]
    print('unit6:', unit6.region)
    
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
    test_create_units(game, 5)
    print('-----SUPPORT UNITS TEST 6-----')

    # Edin
    unit1 = game.players[0].units[0]
    print('unit1:', unit1.region)
    # Clyde
    unit2 = game.players[0].units[1]
    print('unit2:', unit2.region)
    # Yorkshire
    unit3 = game.players[1].units[0]
    print('unit3:', unit3.region)
    # Norwegian Sea
    unit4 = game.players[1].units[1]
    print('unit4:', unit4.region)
    # Norwegian Sea
    unit5 = game.players[1].units[2]
    print('unit5:', unit5.region)
    
    order1 = Hold(0, 'Edinburgh')
    order2 = Support(0, 'Clyde', from_='Edinburgh', to='Edinburgh')
    order3 = Hold(1, 'Yorkshire')
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
    assert game.game_map.regions['Edinburgh'].unit == hash(unit5)
    assert game.game_map.regions['Yorkshire'].unit == hash(unit4)
    assert game.game_map.regions['Liverpool'].unit == None
    assert game.game_map.regions['Norwegian Sea'].unit == None
    assert game.game_map.regions['North Sea'].unit == hash(unit6)

    assert [key for key in game.game_map.dislodged.keys()][0] == hash(unit1)


    print('-----SUPPORT UNITS TEST 6 PASSED-----')

