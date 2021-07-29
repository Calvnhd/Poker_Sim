import game

def start_game(names):
    g = game.Game(names)
    done = False
    i = 0
    while not done:
        print('\n***********************************  Game ' + str(i) + ' ***********************************')

        g.deal() # deal & blinds
        print(g.info())
        print('\nPre-Flop Actions ====================')
        results = g.players_act()
        print('=====================================')
        print('Pre-Flop results: ' + str(results))
        print('=====================================\n')
        g.update_round()

        print('Game sees ' + str(g.count_active_players()) + ' active players remaining before Flop')
        if g.count_active_players() > 1:
            g.deal() # flop
            print(g.info())
            print(g.hand_info())
            print('\nFlop Actions ========================')
            results = g.players_act()
            print('=====================================')
            print('Flop results: ' + str(results))
            print('=====================================\n')
            g.update_round()
            
            print('Game sees ' + str(g.count_active_players()) + ' active players remaining before Turn')
            if g.count_active_players() > 1:
                g.deal() # turn
                print(g.info())
                print(g.hand_info())
                print('\nTurn Actions ========================')
                results = g.players_act()
                print('=====================================')
                print('Turn results: ' + str(results))
                print('=====================================\n')
                g.update_round()

                print('Game sees ' + str(g.count_active_players()) + ' active players remaining before Turn')
                if g.count_active_players() > 1:
                    g.deal() # river
                    print(g.info())
                    print(g.hand_info())
                    print('\nRiver Actions =======================')
                    results = g.players_act()
                    print('=====================================')
                    print('River results: ' + str(results))
                    print('=====================================\n')
                    g.update_round()

        print('\n***** END OF HAND *****')
        print('Game sees ' + str(g.count_active_players()) + ' active players at end')
        if g.count_active_players() > 1:
            print('SHOWDOWN!')
        g.find_leaders()
        print('... Awarding pot ...')
        print(g.award_pot())

        g.update_positions()
        if (g.is_game_over()):
            print('\n--- Only one player remaining.  Game over after ' + str(i) + ' hands ---')
            print(g.info())
            done = True

        i += 1

        ### for testing
        if i > 10:
            print('\n--- loop killed by max i = ' + str(i) + ' ---')
            print(g.info())
            done = True