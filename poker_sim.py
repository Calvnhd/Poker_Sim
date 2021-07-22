import random
# milestone 1 tbc -- generate a large number of hands, rank them all and display
# milestone -- automate one six player game worth of hands, rank, print result

# Deck of cards class
# 52 Cards of [rank,suit] in a nested list [[r,s],[r,s],[r,s]...]
class Deck:
    def __init__(self):
        self.deck = []      # Track cards in deck
        self.removed = []   # Track cards pulled from deck (in play and discarded)

        # Build deck
        suit = 'H'
        for card in range(2,15):
            self.deck.extend([[card, suit]])
        suit = 'D'
        for card in range(2,15):
            self.deck.extend([[card, suit]])
        suit = 'C'
        for card in range(2,15):
            self.deck.extend([[card, suit]])
        suit = 'S'
        for card in range(2,15):
            self.deck.extend([[card, suit]])
    def get_size(self):         # Get number of cards (remaining) in deck
        return len(self.deck)
    def get_removed_size(self): # Get number of cards removed from deck
        return len(self.removed)
    def shuffle(self):          # Recombine all cards into deck and shuffle
        shuffled = []
        if len(self.removed) > 0:
            self.deck.extend(self.removed)
            self.removed = []
        for card in range(len(self.deck)):
            shuffled.append(self.deck.pop(random.randint(0, len(self.deck)-1)))
        self.deck = shuffled[:]
        if len(self.deck) != 52:
            print("WARNING: something has gone wrong with your shuffling") # Figure out how to throw proper error messages and update this
    def take_card(self):        # Take card from top of deck (removed card tracked in removed[])
        card = self.deck.pop(0)
        self.removed.append(card)
        return card
    def get_deck(self):        # Cards (remaining) in deck
        return self.deck
    def get_removed(self):     # Cards removed from deck
        return self.removed
    def info(self):             # Print number of cards remaining & removed
        info = 'Number of cards...\nRemaining: ' + str(len(self.deck)) + '\nRemoved: ' + str(len(self.removed))
        return info

# Evaluates a five card hand
# Takes list of ranks & suits [[r,s],[r,s],[r,s],[r,s],[r,s]]
# Returns evaluation code [hand_ranking, same_hand_comparison, kickers]
# Need to update to compare value of same hands
def evaluate_hand(hand):
    if not (len(hand) == 5):
        print('ERROR COMPARING HANDS')
        return -1
    # Bool for making a hand
    quads = False
    trips = False
    pair_one = False
    pair_two = False
    flush = False
    straight = False
    # Values to compare same hand
    kickers = []
    fh_compare = [0,0]  # stores [trip,pair]
    quad_compare = 0   
    trip_compare = 0
    two_pair_compare = [0,0]
    pair_compare = 0
    # For counting duplicate cards
    count = []
    # Returning value
    value = [0]  

    ranks = set()    
    ranks_all = []
    suits = set()
    for i in range(len(hand)):
        ranks.add(hand[i][0])               # unordered ranks without duplicates
        ranks_all.append(hand[i][0])        # unordered ranks with duplicates
        suits.add(hand[i][1])               # unordered suits
    ranks_sorted = sorted(ranks)            # low to high ranks without duplicates
    ranks_sorted_all = sorted(ranks_all)    # low to high ranks with duplicates

    if len(suits) == 1:  # Check for flush
        flush = True
    if len(ranks) == 5:  # Check for straight
        if ranks_sorted[4] == 14 and ranks_sorted[3] == 5: # Ace is low
            ranks_sorted[4] = 1
            ranks_sorted = sorted(ranks_sorted)
        if ((ranks_sorted[0] + 1) == ranks_sorted[1]) and ((ranks_sorted[1] + 1) == ranks_sorted[2]) and ((ranks_sorted[2] + 1) == ranks_sorted[3]) and ((ranks_sorted[3] + 1) == ranks_sorted[4]):
            straight = True
        else: # High Card
            kickers = sorted(ranks, reverse=True)
    else: 
        # count duplicate cards
        for i in range(len(ranks_sorted)): 
            c = 0
            for j in range(len(ranks_sorted_all)):
                if ranks_sorted_all[j] == ranks_sorted[i]:
                    c += 1
            count.append(c)
        # Find quads / trips / pairs based on final count value
        for i in range(len(count)):
            if count[i] == 1: 
                kickers.append(ranks_sorted[i])
            elif count[i] == 4:
                quads = True
                quad_compare = ranks_sorted[i]
            elif count[i] == 3:
                trips = True
                fh_compare[0] = ranks_sorted[i]
                trip_compare = ranks_sorted[i]
            elif count[i] == 2 and not pair_one:
                pair_one = True
                pair_compare = ranks_sorted[i]
                fh_compare[1] = ranks_sorted[i]
            elif count[i] == 2 and pair_one:
                pair_two = True
                two_pair_compare[0] = pair_compare
                two_pair_compare[1] = ranks_sorted[i]

        kickers = sorted(kickers, reverse=True)

    # print('Contains ranks ' + str(ranks_sorted) + ' occurring ' + str(count) + ' times respectively.   Kickers: ' + str(kickers))

    # Determine value
    if flush and straight and (max(ranks_sorted) == 14):  # Royal Flush
        value[0] = 9
        value.append(max(ranks_sorted))
        return value
    if flush and straight: # Straight Flush
        value[0] =  8
        value.append(max(ranks_sorted)) # use sorted var to account for possible low Ace
        return value
    elif quads: # Four of a Kind
        value[0] =  7
        value.append(quad_compare)
        value.extend(kickers) 
        return value
    elif trips and (pair_one or pair_two): # Full House
        value[0] =  6
        value.extend(fh_compare)
        return value
    elif flush:  # Flush
        value[0] =  5
        value.extend(kickers)
        return value
    elif straight: # Straight
        value[0] =  4
        value.append(max(ranks_sorted)) # use sorted var to account for possible low Ace
        return value
    elif trips: # Three of a kind
        value[0] =  3
        value.append(trip_compare)
        value.extend(kickers)
        return value
    elif pair_one and pair_two: # Two Pair
        value[0] =  2
        two_pair_compare = sorted(two_pair_compare, reverse=True)
        value.extend(two_pair_compare)
        value.extend(kickers)
        return value
    elif pair_one or pair_two: # Pair
        value[0] =  1
        value.append(pair_compare)
        value.extend(kickers)
        return value
    else: # High Card
        value.extend(kickers)
        return value

# takes code from evaluate_hand and returns its meaning in a string
def interpret_eval(hand):
    x = hand[:] 
    for i in range(1, len(x)):
        if x[i] == 11:
            x[i] = 'J'
        elif x[i] == 12:
            x[i] = 'Q'
        elif x[i] == 13:
            x[i] = 'K'
        elif x[i] == 14:
            x[i] = 'A'
        
    #Output message
    if x[0] == 9:
        output = 'Royal Flush!'
    elif x[0] == 8 and len(x) == 2:
        output = 'Straight Flush, ' + str(x[1]) + ' high'
    elif x[0] == 7 and len(x) == 3:
        output = 'Four of a Kind, ' + str(x[1]) + 's with ' + str(x[2]) + ' kicker'
    elif x[0] == 6 and len(x) == 3:
        output = 'Full House, ' + str(x[1]) + 's full of ' + str(x[2]) + 's'
    elif x[0] == 5 and len(x) == 6:
        output = 'Flush, ' + str(x[1]) + ' high followed by ' + str(x[2]) + ' ' + str(x[3]) + ' ' +  str(x[4]) + ' ' +  str(x[5])
    elif x[0] == 4 and len(x) == 2:
        output = 'Straight, ' + str(x[1]) + ' high'
    elif x[0] == 3 and len(x) == 4:
        output = 'Three of a Kind, ' + str(x[1]) + 's with ' + str(x[2]) + ' ' + str(x[3]) + ' kickers'
    elif x[0] == 2 and len(x) == 4:
        output = 'Two Pair, ' + str(x[1]) + 's and ' + str(x[2]) + 's with ' + str(x[3]) + ' kicker'
    elif x[0] == 1  and len(x) == 5:
        output = 'Pair of ' + str(x[1]) + 's, with '+ str(x[2]) + ' ' + str(x[3]) + ' ' + str(x[4]) + ' kickers'
    elif x[0] == 0 and len(x) == 6:
        output = str(x[1]) + ' High, followed by ' + str(x[2]) + ' ' + str(x[3]) + ' ' + str(x[4]) + ' ' + str(x[5])
    else:
        output = 'ERROR INTERPRETTING HAND EVALUATION CODE'
    return output

# Compares hands h1 and h2.  5 cards in each.
# h1 and h2 must be output from evaluate_hand
# returns the best of h1 or h2 in the same format as input, or 0 if they are equal
def compare_hands(h1, h2, i=0):
    if i == 7: # Base case
        print('ERROR COMPARING HANDS')
        return -1
    if h1 == h2:
        return 0
    if h1[i] > h2[i]:
        return h1
    elif h1[i] < h2[i]:
        return h2
    else:
        if h1[i] == h2[i] and len(h1) == len(h2):
            i += 1
            return compare_hands(h1,h2,i)
        else:
            print('ERROR COMPARING HANDS')
            return -1

# Finds the best hand a player can make with their 2 cards
# takes 2 cards from hand, 3 to 5 cards from board, and returns the best hand in the form of eval code
def make_hands(H, B):
    h = []
    b = []
    best = []
    test = []

    # Ensure correct inputs and initialize best
    if len(H) == 2 and len(B) > len(H):
        h = H[:]
        b = B[:]
    elif len(B) == 2 and len(H) > len(B): 
        h = B[:]
        b = H[:]
    else:
        print('ERROR:  Incorrect input.')
        return -1
    # initialize best 5 to hand and flop
    best.extend(h)
    best.extend([b[0], b[1], b[2]])
    el_best = evaluate_hand(best)

    # Find best 5 card combination
    if (len(h) + len(b)) == 5: # 3 cards on board (flop)
        return el_best
    elif (len(h) + len(b)) == 6: # 4 cards on board (turn)
        for i in range(6):
            test = []
            if i < 2:
                test.append(h[i]) # using just one card from hand
                test.extend(b)
                el_test = evaluate_hand(test)
                comp = compare_hands(el_test, el_best) # returns eval of best, or 0 if equal 
                if comp != 0:
                    el_best = comp
            else:
                test.extend(h)  # using both cards in hand
                hold = b[:]     # copy data to keep original board info b[] intact
                hold.pop(i-2)   # select three of the four cards on board by removing one
                test.extend(hold)
                el_test = evaluate_hand(test)
                comp = compare_hands(el_test, el_best)
                if comp != 0:
                    el_best = comp
        return el_best
    elif (len(h) + len(b)) == 7: # 5 cards on board (river)
        for i in range(4):
            for j in range(5):
                test = []   # reset test hand
                if i < 2:   # use one card in hand
                    test.append(h[i])   # one card from hand (i = 0 or 1)
                    hold = b[:]
                    hold.pop(j)         # pop off one of 5 (j = 0 to 4) on board, to select 4 remaining cards 
                    test.extend(hold)   # test hand built
                    el_test = evaluate_hand(test)
                    comp = compare_hands(el_test, el_best)
                    if comp != 0:
                        el_best = comp
                if i == 2:  # use both cards in hand 
                    for k in range(5):
                        test = []
                        test.extend(h)  # both cards
                        hold1 = b[:]
                        hold2 = []
                        if k > j : # use j and k to select cards to pop
                            # i j k
                            # where i == both from hand, and j k indicate which cards from board NOT to include
                            # print('ijk: ' + str(i) + ' ' + str(j) + ' ' + str(k))
                            # find unwanted cards
                            for x in range(len(hold1)):
                                if x == k or x == j:
                                    hold1[x] = -1
                            # rebuild without unwanted cards
                            for x in range(len(hold1)):
                                if hold1[x] != -1:
                                    hold2.append(hold1[x])
                            if len(hold2) != 3:
                                print('ERROR CHOOSING CARDS FROM BOARD')
                            test.extend(hold2)
                            el_test = evaluate_hand(test)
                            comp = compare_hands(el_test, el_best)
                            if comp != 0:
                                el_best = comp
                        else:
                            pass
                if i == 3:  # no cards from hand
                    test.extend(b)
                    el_test = evaluate_hand(test)
                    comp = compare_hands(el_test, el_best)
                    if comp != 0:
                        el_best = comp
        return el_best            
    else:
        print('ERROR B:  Incorrect input.')
        return -1

# Takes a list of evaluated hands, and returns the best one
# Try different sorting algorithms?
def find_best_hand(hands):
    best = hands[0]
    if len(hands) > 1:
        for h in range(1, len(hands)):
            comp = compare_hands(best, hands[h])
            if comp != 0:
                best = comp
    return best

# Expand using inheritance to add different player archetypes
class Player:
    def __init__(self, name, chips, position):
        self.name = name
        self.chips = chips
        self.hand = []
        self.position = position
    def get_chips(self):
        return self.chips
    def bet(self, amount):  # need to check that betting won't be more than total chips
        self.chips -= amount
        return amount
    def add_chips(self, amount):
        self.chips += amount
    def info(self):
        return ('Name: ' + str(self.name) + '  ...  Chips: $' + str(self.chips) + '  ...  Hand: ' + str(self.hand) + '  ...  Position: ' + str(self.position))
    def set_position(self, position):
        self.position = position
    def get_position(self):
        return self.position
    def give_card(self, card):
        self.hand.append(card)
    def get_hand(self):
        return self.hand
    def reset_hand(self):
        self.hand = []
    def get_name(self):
        return str(self.name)

# Holds all ongoing game elements
# Players (name, hand, chips, positions), leaders, chip_leaders, Deck, board, pot
class Game:
    def __init__(self, names):
        self.names = names  # add check for duplicate names, and min/max players
        self.player_count = len(self.names) 
        # initialze deck 
        self.deck = Deck()
        self.deck.shuffle()
        # hardcode chips and blinds
        self.starting_stack = 300
        self.total_chips = int(self.starting_stack * self.player_count)
        self.bb = 2               
        self.sb = int(self.bb/2)
        # create players and store in list
        self.players = []
        for i in range(self.player_count):
            self.players.append(Player(self.names[i], self.starting_stack, i))  # find a way to randomize starting dealer pos
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
        # info = 'Pot: ' + str(self.pot) + '\n'
        info = ''
        for i in range(self.player_count):
            info += self.players[i].info()
            info += '\n'
        info += ('Board: ' + str(self.board) + '\n')
        info += ('Pot: $' + str(self.pot))
        return info
    def update_positions(self): # Shifts dealer button by updating pos for each player in players list
        for i in range(self.player_count):
            if self.players[i].get_position() == self.player_count - 1: # if at max pos
                self.players[i].set_position(0)                         # set pos to 0 (dealer)
            else:    
                pos = self.players[i].get_position() + 1
                self.players[i].set_position(pos)
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
        if self.pot != 0 and self.round == 0:
            print('ERROR!  POT NOT TAKEN BEFORE NEXT DEAL')
            self.pot = 0
        if self.round == 0:   # Deal
            # print('NEW DEAL')
            # Reset for new hand
            self.board = []
            self.deck.shuffle()
            for i in range(self.player_count):
                self.players[i].reset_hand()
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
            self.round += 1
        elif self.round == 1:  # Flop
            self.deck.take_card()   # Burn a card
            for i in range(3):      # Add 3 cards to board
                self.board.append(self.deck.take_card())
            self.round += 1
        elif self.round == 2:  # Turn
            self.deck.take_card()                       # Burn a card
            self.board.append(self.deck.take_card())    # Add one card to board
            self.round += 1
        elif self.round == 3:  # River
            self.deck.take_card()                       # Burn a card
            self.board.append(self.deck.take_card())    # Add one card to board
            self.round = 0
        else:
            print('\nDEALING ERROR')
    def get_deck(self): # returns list of cards remaining in deck
        return self.deck.get_deck()
    def get_removed(self): # returns list of cards removed from deck 
        return self.deck.get_removed()
    def get_board(self): # returns list of cards on board
        return self.board
    def get_round(self): # returns int corresponding to betting round.  Increments with each deal() call from 0 (Pre-Flop) to 3 (River).
        return round
    def award_pot(self): # gives / splits pot to those in leaders[], matching names with players[].  Returns string with award info. Does not yet account for side pots!
        chips = int(self.pot / len(self.get_leaders()))
        if len(self.get_leaders()) > 1:
            output = '$' + str(chips) + ' each to '
        else: 
            output = '$' + str(chips) + ' to '
        i = (len(self.get_leaders()) - 1)
        while i >= 0:
            for j in range(self.player_count):
                if self.leaders[i].get_name() == self.players[j].get_name():
                    self.players[j].add_chips(chips)
                    output += str(self.players[j].get_name())
                    output += ' '
            i -= 1
        self.pot = 0
        return output
    def find_leaders(self): # creates list hands[] of best 5 card hand for each player, finds best_hand overall, and creates list leaders[] of player objects who hold the best hand 
        self.leaders = []
        if len(self.board) < 3:
            print('ERROR! NOT ENOUGH CARDS ON BOARD TO MAKE HANDS')
        else: 
            # Find the best 5 card hand from each player
            self.hands = []
            for i in range(self.player_count):
                self.hands.append(make_hands(self.players[i].get_hand(), self.board))
            self.best_hand = find_best_hand(self.hands)
            # Match player hand to best hand
            for i in range(self.player_count):
                if self.best_hand == self.hands[i]:
                    self.leaders.append(self.players[i])
    def get_player_hands(self): # returns hands[] as created in find_leaders()
        if self.player_count != len(self.hands):
            self.find_leaders()
        return self.hands
    def get_leaders(self): # returns leaders[] as created in find_leaders()
        if self.player_count != len(self.hands):
            self.find_leaders()
        return self.leaders
    def hand_info(self):
        output = ''
        if len(self.board) >= 3:
            if self.player_count != len(self.hands):
                self.find_leaders()
            for i in range(self.player_count):
                output += (str(self.players[i].get_name()) + ': ' + interpret_eval(self.hands[i]) + '\n')
            output += ('Best hand: ' + str(interpret_eval(self.best_hand))) 
        else:
            output = "ERROR! CAN'T PRINT HAND INFO PRE-FLOP"
        return output

game = Game(['CD', 'IK', 'BM'])
for i in range(100):
    print('====  Game ' + str(i) + ' ====')
    game.deal() # deal & blinds
    game.deal() # flop
    game.deal() # turn
    game.deal() # river
    game.find_leaders()

    print('...Results... ')
    print(game.info())
    print(game.hand_info())

    print(game.award_pot())
    game.update_positions()


