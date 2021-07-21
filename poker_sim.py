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
    def list_deck(self):        # Print cards (remaining) in deck
        print(self.deck)
    def list_removed(self):     # Print cards removed from deck
        print(self.removed)
    def info(self):             # Print number of cards remaining & removed
        print('Number of cards...')
        print('Remaining: ' + str(len(self.deck)))
        print('Removed: ' + str(len(self.removed)))

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
        print('ERROR A:  Incorrect input.')
        return -1
    # initial best 5: hand and flop
    best.extend(h)
    best.extend([b[0], b[1], b[2]])
    el_best = evaluate_hand(best)
    print('init best: ' + str(el_best) + ' == ' + interpret_eval(el_best))

    # Find best 5 card combination
    if (len(h) + len(b)) == 5: # 3 cards on board (flop)
        print('making hands -- FLOP')
        return el_best
    elif (len(h) + len(b)) == 6: # 4 cards on board (turn)
        print('making hands -- TURN')
        for i in range(6):
            test = []
            print('          **** at i == ' + str(i) + ' ****')
            print('Current best: ' + str(el_best) + ' == ' + interpret_eval(el_best))
            if i < 2:
                test.append(h[i]) # using just one card from hand
                test.extend(b)
                el_test = evaluate_hand(test)
                print('THIS TEST: ' + str(test))
                print('Test eval: ' + str(el_test) + ' == ' + interpret_eval(el_test))

                comp = compare_hands(el_test, el_best) # returns eval of best, or 0 if equal 
                if comp != 0:
                    el_best = comp
                    print('Best is ' + str(el_best) + ' == ' + interpret_eval(el_best))
            else:
                test.extend(h)  # using both cards in hand
                hold = b[:]     # copy data to keep original board info b[] intact
                hold.pop(i-2)   # select three of the four cards on board
                test.extend(hold)
                el_test = evaluate_hand(test)
                print('THIS TEST: ' + str(test))
                print('Test eval: ' + str(el_test) + ' == ' + interpret_eval(el_test))

                comp = compare_hands(el_test, el_best)
                if comp != 0:
                    print('Best is ' + str(el_best) + ' == ' + interpret_eval(el_best))
                    el_best = comp
        return el_best
    elif (len(h) + len(b)) == 7: # 5 cards on board (river)
        print('making hands -- RIVER')
        for i in range(7):
            test = []
    else:
        print('ERROR B:  Incorrect input.')
        return -1


# Expand using inheritance to add different player archetypes
class Player:
    def __init__(self, name, chips, position):
        self.name = name
        self.chips = chips
        self.hand = []
        self.position = position
    def get_chips(self):
        return self.chips
    def bet(self, amount):
        self.chips -= amount
        return amount
    def add_chips(self, amount):
        self.chips += amount
    def get_info(self):
        print('Name: ' + str(self.name) + '  ...  Chips: ' + str(self.chips) + '  ...  Hand: ' + str(self.hand) + '  ...  Position: ' + str(self.position))
    def set_position(self, position):
        self.position = position
    def give_card(self, card):
        self.hand.append(card)
    def get_hand(self):
        return self.hand

# Update to pass in variables of game for re-useability
def print_game_details():
    print('\n===  Player Status ===')
    print(str(player_count) + ' Players')
    p1.get_info()
    p2.get_info()
    p3.get_info()
    print('Pot: ' + str(pot))

print("\n ===== Welcome to Calvin's Poker Simulator! =====")

player_count = 3
starting_stack = 300
bb = 2
sb = int(bb /2)

# Update this with a for loop to have a flexible number of players (3 to 8)
p1 = Player('Calvin', starting_stack, 0)
p2 = Player('Ian', starting_stack, 1)
p3 = Player('Beattie', starting_stack, 2)
players = [p1, p2, p3]



# Deal a hand
# figure out how to break this into loopable steps
deck = Deck()
deck.shuffle()
board = []
pot = 0
# Deal
for i in range(player_count):
    players[i].give_card(deck.take_card())
for i in range(player_count):
    players[i].give_card(deck.take_card())

pot += players[1].bet(sb)
pot += players[2].bet(bb)

# Flop
deck.take_card() #Burn
board.append(deck.take_card())
board.append(deck.take_card())
board.append(deck.take_card())

print_game_details()

print('============')
player_best = make_hands(p1.get_hand(), board)
print('\nRESULTS:\np1 (Calvin) hand: ' +  str(p1.get_hand()))
print('board: ' + str(board))
print('current p1 best: ' + str(player_best) + ' -- ' + interpret_eval(player_best))
print('')

# Turn
deck.take_card() #Burn
board.append(deck.take_card())

print('============')
player_best = make_hands(p1.get_hand(), board)
print('\nRESULTS:\np1 (Calvin) hand: ' +  str(p1.get_hand()))
print('board: ' + str(board))
print('current p1 best: ' + str(player_best) + ' -- ' + interpret_eval(player_best))
print('')

# River
deck.take_card() #Burn
board.append(deck.take_card())

print('============')
player_best = make_hands(p1.get_hand(), board)
print('\nRESULTS:\np1 (Calvin) hand: ' +  str(p1.get_hand()))
print('board: ' + str(board))
print('current p1 best: ' + str(player_best) + ' -- ' + interpret_eval(player_best))
print('')

# for testing hand
# eval = -1
# test_deck = Deck()
# count = 0

# eval_code = []
# while eval != 100:
#     count += 1
#     for i in range(7):
#         test_deck.shuffle()

#     h1 = []
#     h2 = []
#     for i in range(5):
#         h1.append(test_deck.take_card())
#         h2.append(test_deck.take_card())

#     e_h1 = evaluate_hand(h1)
#     e_h2 = evaluate_hand(h2)

#     print('\nh1: ' + str(h1)) 
#     print(interpret_eval(e_h1))
#     print('h2: ' + str(h2))
#     print(interpret_eval(e_h2))

#     comp = compare_hands(e_h1, e_h2)
#     if comp == 0:
#         print('These hands are equal\n')
#     else:
#         print('Winner: ' + interpret_eval(comp))
    
#     eval +=1

# # print('...found after ' + str(count) + ' hands')


# notes
# use a dictionary for player names and positions?
