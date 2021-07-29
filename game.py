import cards
import player

# Holds all ongoing game elements
# Players (name, hand, chips, positions), leaders, chip_leaders, Deck, board, pot
class Game:
    def __init__(self, names):
        self.names = names  # add check for duplicate names, and min/max players
        self.player_count = len(self.names) 
        # initialze deck 
        self.deck = cards.Deck()
        self.deck.shuffle()
        # hardcode chips and blinds
        self.starting_stack = 300
        self.total_chips = int(self.starting_stack * self.player_count)
        self.bb = 2               
        self.sb = int(self.bb/2)
        # create players and store in list
        self.players = []
        for i in range(self.player_count):
            self.players.append(player.Player(self.names[i], self.starting_stack, i))  # find a way to randomize starting dealer pos
        # additional items to track
        self.leaders = []       # players with winning hands
        self.hands = []         # stores best hand of players[i] as eval code
        self.best_hand = []     # stores the best hand overall
        self.chip_leaders = []  # players with most chips
        self.board = []         # cards on board for a round
        self.pot = 0            # current pot for given betting round
        self.round = 0          # update for deal, flop ,turn, river            
    def get_players(self): # Returns a list of the player objects
        return self.players
    def info(self):  # Returns a string showing pot, players object info (name,chips,hand,pos), cards on board
        info = ''
        for i in range(self.player_count):
            info += self.players[i].info()
            info += '\n'
        info += ('Board: ' + str(self.board) + '\n')
        info += ('Pot: $' + str(self.pot))
        return info
    def update_positions(self): # Shifts dealer button by updating pos for each player in players list, resets active status for players with chips remaining, and sets round to 0
        for i in range(self.player_count):
            if self.players[i].get_position() == self.player_count - 1: # if at max pos
                self.players[i].set_position(0)                         # set pos to 0 (dealer)
            else:    
                pos = self.players[i].get_position() + 1
                self.players[i].set_position(pos)
            if self.players[i].get_chips() > 0:
                print(str(self.players[i].get_name()) + ' has ' + str(self.players[i].get_chips()) + ' chips remaining')
                self.players[i].set_active(True)
        self.round = 0
    def update_round(self): # increments round, or returns to zero for new deal
        if self.round == 3:
            self.round = 0
        else:
            self.round += 1
        # print('Setting round to ' + str(self.round) + ' in game.update_round')
        return self.round
    def get_chip_leaders(self): # Returns a list of players objects with the most chips
        self.chip_leaders = []
        max = 0
        for i in range(self.player_count): # find biggest stack
            if (self.players[i].get_chips()) >= max:
                max = self.players[i].get_chips()
        for i in range(self.player_count):
            if (self.players[i].get_chips()) == max:
                self.chip_leaders.append(self.players[i].get_name())
        return self.chip_leaders
    def deal(self): # the core step in the Game. Loop through to deal cards to players and post blinds, flop, river, turn.  Tracks betting rounds and acts accordingly.
        # update to skip dealing to inactive players Pre-Flop?  This matters for realism only.
        # if self.pot != 0 and self.round == 0:
        #     print('ERROR!  POT NOT TAKEN BEFORE NEXT DEAL')
        #     self.pot = 0
        if self.round == 0:   # Deal
            print('NEW DEAL')
            # Reset for new hand
            self.board = []
            self.deck.shuffle()
            for i in range(self.player_count):
                self.players[i].reset_hand()
                if self.players[i].get_chips() > 0: # This is also done by update_position
                    self.players[i].set_active(True)
                else:
                    self.players[i].set_active(False)   
            # Find who sits (index of players[i]) to the left of dealer (position 1)
            seat = -1
            i = 0
            while (seat == -1) and (i < 30):
                pos = self.players[i].get_position()
                if pos == 1:
                    seat = i
                i += 1
            # deal i = 2 cards to each of j players, starting from dealer's left
            for i in range(2):
                for j in range(self.player_count):
                    if (seat + j) < self.player_count:
                        self.players[(seat+j)].give_card(self.deck.take_card())
                    elif (seat + j) >= self.player_count:
                        self.players[(seat + j - self.player_count)].give_card(self.deck.take_card())
            # Post blinds
            for i in range(self.player_count):
                if self.players[i].get_position() == 1:
                    # print('Small blind: ' + self.players[i].get_name())
                    self.pot += self.players[i].bet(self.sb)
                if self.player_count > 2:
                    if self.players[i].get_position() == 2:
                        # print('Big blind: ' + self.players[i].get_name())
                        self.pot += self.players[i].bet(self.bb)
                elif self.player_count == 2:
                    if self.players[i].get_position() == 0:
                        # print('Big blind: ' + self.players[i].get_name())
                        self.pot += self.players[i].bet(self.bb)
                else:
                    print('ERROR POSTING BLINDS.  ONLY ONE PLAYER.')
        elif self.round == 1:  # Flop
            print('DEALING FLOP')
            self.deck.take_card()   # Burn a card
            for i in range(3):      # Add 3 cards to board
                self.board.append(self.deck.take_card())
        elif self.round == 2:  # Turn
            print('DEALING TURN')
            self.deck.take_card()                       # Burn a card
            self.board.append(self.deck.take_card())    # Add one card to board
        elif self.round == 3:  # River
            print('DEALING RIVER')
            self.deck.take_card()                       # Burn a card
            self.board.append(self.deck.take_card())    # Add one card to board
        else:
            print('\nDEALING ERROR.  Rounds not set')
    def get_deck(self): # returns list of cards remaining in deck
        return self.deck.get_deck()
    def get_removed(self): # returns list of cards removed from deck 
        return self.deck.get_removed()
    def get_board(self): # returns list of cards on board
        return self.board
    def get_round(self): # returns int from 0 (Pre-Flop) to 3 (River) corresponding to betting round. Increment with update_round()
        return self.round
    def award_pot(self): # gives / splits pot to those in leaders[], matching names with players[].  Returns string with award info. Does not yet account for side pots!
        print('Calling award_pot')
        chips = int(self.pot / len(self.leaders))
        if len(self.leaders) > 1:
            output = '$' + str(chips) + ' each to '
        else: 
            output = '$' + str(chips) + ' to '
        i = (len(self.leaders) - 1)
        while i >= 0:
            for j in range(self.player_count):
                if self.leaders[i].get_name() == self.players[j].get_name():
                    self.players[j].add_chips(chips)
                    output += str(self.players[j].get_name())
                    output += ' '
            i -= 1
        if self.pot % len(self.leaders) != 0:
            self.pot = self.pot % len(self.leaders) # add leftover chips back into pot for next round
        else:
            self.pot = 0
        return output
    def chips_check(self):
        chips = self.pot
        for i in range(self.player_count):
            if self.players[i].get_chips() < 0:
                print('ERROR! Player has negative chips')
            else:
                chips += self.players[i].get_chips()
        if chips != self.total_chips:
            print('ERROR! Incorrect number of total chips')
            for i in range(self.player_count):
                print(str(self.players[i].get_name()) + ': ' + str(self.players[i].get_chips()) + ' chips')
            print('Pot: ' + str(self.pot))
    def find_leaders(self): # creates list hands[] of best 5 card hand (in eval code) for each player, sets best_hand for player object, finds best_hand overall, and creates list leaders[] of player objects who hold the best hand 
        print('Calling find_leaders')
        self.leaders = []
        names = []
        if self.count_active_players() == 1:
            print('find_leaders sees only 1 player active')
            for i in range(self.player_count):
                if self.players[i].is_active() == True:
                    self.leaders.append(self.players[i])
                    names.append(self.players[i].get_name())
        else: 
            # Find the best 5 card hand from each player and store in hands[]
            # Player objects could do this part??
            self.hands = []
            for i in range(self.player_count):
                if self.players[i].is_active():  # exclude inactive players
                    self.hands.append(cards.make_hands(self.players[i].get_hand(), self.board))
                    self.players[i].set_best_hand(self.hands[i])
                else:
                    self.hands.append([0,0,0]) # folded hand
                    self.players[i].set_best_hand([0,0,0])
                self.best_hand = cards.find_best_hand(self.hands)
            print('Player hands: ' + str(self.hands))
            print('Best hand: ' + str(self.best_hand) + ' ... ' + str(cards.interpret_eval(self.best_hand)))
            # Match player hand to best hand
            for i in range(self.player_count):
                if self.best_hand == self.players[i].get_best_hand():
                    self.leaders.append(self.players[i])
                    names.append(self.players[i].get_name())
        print('Leaders: ' + str(names))
    def get_player_hands(self): # returns hands[] as created in find_leaders()
        if self.player_count != len(self.hands):
            self.find_leaders()
        return self.hands
    def get_leaders(self): # returns leaders[] as created in find_leaders()
        if self.player_count != len(self.hands):
            print('Calling find_leaders from get_leaders')
            self.find_leaders()
        return self.leaders
    def hand_info(self): # returns string of best hand made by each player
        output = ''
        if self.round != 0:
            self.find_leaders()
            for i in range(self.player_count):
                output += (str(self.players[i].get_name()) + ': ' + cards.interpret_eval(self.players[i].get_best_hand()) + '\n')
            output += ('Best hand: ' + str(cards.interpret_eval(self.best_hand))) 
        else:
            output = "ERROR! CAN'T PRINT HAND INFO PRE-FLOP"
        return output
    def count_active_players(self):
        c = 0
        for i in range(self.player_count):
            if self.players[i].is_active() == True:
                c += 1
        return c
    def players_act(self):  # Instructs players to act in turn.  Return [0]: continue dealing or award pot, winner and amount ['award','name',int]
        # initialize values
        end_name = 0
        player_bets = []  # track how many chips a player has committed per betting round
        # player_turn_count = [] # track how many turns a player has taken.  Not sure if you need this??
        for i in range(self.player_count):
            player_bets.append(0)
            # player_turn_count.append(0)
        if self.round == 0: # post blinds and UTG start position 
            current_bet = self.bb
            prev_raise = self.bb
            # find left of bb (UTG: Under The Gun)
            if self.player_count > 3:
                player_turn = 3
            elif self.player_count == 3:
                player_turn = 0
            elif self.player_count == 2:
                player_turn = 1
            # find sb and bb and add to player_bets[].  Update to kill loop when sum of player_bets[] == sb + bb to avoid unneccessary loops
            for i in range(self.player_count):
                if self.player_count > 2:
                    for j in range(self.player_count):
                        if self.players[j].get_position() == 1:
                            player_bets[j] = self.sb
                        elif self.players[j].get_position() == 2:
                            player_bets[j] = self.bb
                elif self.player_count == 2:
                    for j in range(self.player_count):
                        if self.players[j].get_position() == 1:
                            player_bets[j] = self.sb
                        elif self.players[j].get_position() == 0:
                            player_bets[j] = self.bb
        else:
            current_bet = 0
            prev_raise = 0
            player_turn = 1 # left of dealer
        done = False
        players_active = [] # status of players active or not
        names = []          # just used to print stuff.  Can delete later.
        player_actions = []
        for i in range(self.player_count):
            players_active.append(self.players[i].is_active())
            names.append(self.players[i].get_name())
            if self.players[i].is_active():
                player_actions.append('wait')
            else:
                player_actions.append('fold')
        print('First to act at position ' + str(player_turn))
        w = 0
        # Loop through players, and act if it's their turn
        while not done:
            # look through list of players. 
            for i in range(self.player_count):
                if self.players[i].get_position() == player_turn: # is player's turn
                    pl_prev_bet = player_bets[i]
                    action = []
                    if self.players[i].is_active():
                        # count players still waiting to make turn
                        # not sure if this works when players have folded.  Are they still waiting if folded?
                        waits = 0
                        for j in range(len(player_actions)):
                            if player_actions[j] == 'wait':
                                waits += 1
                        action = self.players[i].action(self.round, self.board, self.pot, self.bb, current_bet, prev_raise, pl_prev_bet, waits)
                        print(' Action: ' + str(action))
                        player_actions[i] = action[0]
                        player_bets[i] = action[1]
                        print('  Names: ' + str(names))
                        print('Actions: ' + str(player_actions))
                        print('   Bets: ' + str(player_bets))
                        if action[0] == 'fold':
                            players_active[i] = False
                        elif action[0] == 'end':
                            # print('End action detected in Game loop at player ' + str(self.players[i].get_name()))
                            end_name = self.players[i].get_name()
                            done = True
                            break
                        # update info for next player decision
                        if action[1] > 0: # bet or call
                            print('adding ' + str(action[1] - pl_prev_bet) + ' to the pot')
                            self.pot += (action[1] - pl_prev_bet) # add bet/call to pot
                            if action[1] > current_bet: # find raise
                                prev_raise = action[1] - current_bet
                                current_bet = action[1]
                    else:
                        print(str(self.players[i].get_name()) + ' is not active (GL)') 

                    if player_turn == self.player_count - 1:
                        player_turn = 0 
                    else: 
                        player_turn += 1
                    print('Next player to act is at position ' + str(player_turn) + '\n')
            w += 1
            # for testing / safety
            if w > 100: 
                print('While loop killed by w > condition')
                done = True
        # check for folds
        folds = 0
        for i in range(len(player_actions)):
            if player_actions[i] == 'fold':
                folds += 1

        print('\nFINISHED TAKING ACTIONS')
        print(player_actions)
        print(player_bets)
        print(players_active)
        print(str(folds) + ' players have folded out of ' + str(len(player_actions)) + ' players')

        if folds == len(player_actions) - 1:
            print('No more dealing needed')
            return ['award',end_name,self.pot]

        return [0]
    def is_game_over(self): # Checks if more than one player has chips remaining
        no_chips = 0
        for i in range(self.player_count):
            if self.players[i].get_chips() == 0:
                no_chips += 1
        if no_chips == self.player_count - 1:
            return True
        else:
            return False
