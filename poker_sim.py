import random

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
# Returns [i,j] where i is hand ranking
# Need to update to compare value of same hands
def evaluate_hand(hand):
    quads = False
    trips = False
    pair_one = False
    pair_two = False
    flush = False
    straight = False
    kickers = []
    fh_compare = [0,0]
    quad_compare = 0
    trip_compare = 0
    two_pair_compare = [0,0]
    pair_compare = 0
    count = []
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

    print('\nAnalyzing... ' + str(hand))

    if len(suits) == 1:  # Check for flush
        flush = True
    if len(ranks) == 5:  # Check for straight
        if ranks_sorted[4] == 14 and ranks_sorted[3] == 5: # Ace is low
            ranks_sorted[4] == 1
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
        # Find quads / trips / pairs
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

    print('Contains ranks ' + str(ranks_sorted) + ' occurring ' + str(count) + ' times respectively.   Kickers: ' + str(kickers))

    # Determine value
    if flush and straight and (max(ranks_sorted) == 14):
        print('Royal Flush')
        value[0] = 9
        value.append(max(ranks_sorted))
        return value
    if flush and straight:
        print('Straight Flush')
        value[0] =  8
        value.append(max(ranks_sorted)) # use sorted var to account for possible low Ace
        return value
    elif quads:
        print('Four of a Kind')
        value[0] =  7
        value.append(quad_compare)
        value.append(max(kickers)) # should only have one value anyway
        return value
    elif trips and (pair_one or pair_two): 
        print('Full House')
        value[0] =  6
        value.append(fh_compare[0]) # change to extend
        value.append(fh_compare[1])
        return value
    elif flush:
        print('Flush')
        value[0] =  5
        value.append(max(ranks_sorted))
        return value
    elif straight:
        print('Straight')
        value[0] =  4
        value.append(max(ranks_sorted)) # use sorted var to account for possible low Ace
        return value
    elif trips:
        print('Three of a Kind')
        value[0] =  3
        value.append(trip_compare)
        value.append(kickers[0]) # change to extend
        value.append(kickers[1])
        return value
    elif pair_one and pair_two:
        print('Two Pair')
        value[0] =  2
        two_pair_compare = sorted(two_pair_compare, reverse=True)
        value.extend(two_pair_compare)
        value.append(kickers[0])
        return value
    elif pair_one or pair_two:
        print('Pair')
        value[0] =  1
        value.append(pair_compare)
        value.extend(kickers)
        return value
    else:
        print('High Card')
        value.append(max(ranks_sorted))
        return value

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

# Update to pass in variables of game for re-useability
def print_game_details():
    print('\n===  Player Status ===')
    print(str(player_count) + ' Players')
    p1.get_info()
    p2.get_info()
    p3.get_info()
    print('Pot: ' + str(pot))

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

# Turn
deck.take_card() #Burn
board.append(deck.take_card())

# River
deck.take_card() #Burn
board.append(deck.take_card())

# for testing hand eval
eval = -1
count = 0
test_deck = Deck()
test_hand = []
straight_ace = False

while eval != 1:
    count += 1

    for i in range(7):
        test_deck.shuffle()
    test_hand = []
    for i in range(5):
        test_hand.append(test_deck.take_card())
    eval_list = evaluate_hand(test_hand)
    print('Eval code: ' + str(eval_list))
    eval = eval_list[0]

print('...found after ' + str(count) + ' hands')


# notes
# use a dictionary for player names and positions?
