import random

class Deck:
    def __init__(self):
        self.deck = []
        self.removed = []
        # try rewriting into one loop with a dict?
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
    def get_size(self):
        return len(self.deck)
    def get_removed_size(self):
        return len(self.removed)
    def shuffle(self):
        shuffled = []
        if len(self.removed) > 0:
            self.deck.extend(self.removed)
            self.removed = []
        for card in range(len(self.deck)):
            shuffled.append(self.deck.pop(random.randint(0, len(self.deck)-1)))
        self.deck = shuffled[:]
        if len(self.deck) != 52:
            print("WARNING: something has gone wrong with your shuffling") # Figure out how to throw proper error messages and update this
    def take_card(self):
        card = self.deck.pop(0)
        self.removed.append(card)
        return card
    def list_deck(self):
        print(self.deck)
    def list_removed(self):
        print(self.removed)
    def info(self):
        print('Number of cards...')
        print('Remaining: ' + str(len(self.deck)))
        print('Removed: ' + str(len(self.removed)))

def evaluate_hand(hand):
    quads = False
    trips = False
    pair_one = False
    pair_two = False
    flush = False
    straight = False
    value = 0

    ranks = set()    
    ranks_all = []
    suits = set()
    for i in range(len(hand)):
        ranks.add(hand[i][0])               # unordered ranks without duplicates
        ranks_all.append(hand[i][0])        # unordered ranks with duplicates
        suits.add(hand[i][1])               # unordered suits
    ranks_sorted = sorted(ranks)            # low to high ranks without duplicates
    ranks_sorted_all = sorted(ranks_all)    # low to high ranks with duplicates

    print('Analyzing... ' + str(hand))

    if len(suits) == 1:  # Check for flush
        flush = True
        value = max(ranks)
    if len(ranks) == 5:  # Check for straight
        if ranks_sorted[4] == 14 and ranks_sorted[3] == 5: # Ace is low
            ranks_sorted[4] == 1
            ranks_sorted = sorted(ranks_sorted)
        if ((ranks_sorted[0] + 1) == ranks_sorted[1]) and ((ranks_sorted[1] + 1) == ranks_sorted[2]) and ((ranks_sorted[2] + 1) == ranks_sorted[3]) and ((ranks_sorted[3] + 1) == ranks_sorted[4]):
            straight = True
            value = max(ranks_sorted)
        else:
            value = max(ranks) # High card
    else: 
        count = []
        kickers = []

        # count duplicate cards
        for i in range(len(ranks_sorted)): 
            c = 0
            for j in range(len(ranks_sorted_all)):
                if ranks_sorted_all[j] == ranks_sorted[i]:
                    c += 1
            count.append(c)

        # determine hand
        for i in range(len(count)):
            if count[i] == 1: 
                kickers.append(ranks_sorted[i])
            elif count[i] == 4:
                quads = True
            elif count[i] == 3:
                trips = True
            elif count[i] == 2 and not pair_one:
                pair_one = True
            elif count[i] == 2 and pair_one:
                pair_two = True       

        print('Contains ranks ' + str(ranks_sorted))
        print('Occurring ' + str(count) + ' respectively')
        print('Kickers: ' + str(kickers))

# calculate value
    if flush and straight and (ranks_sorted[4] == 14):
        print('Royal Flush')
        return 9
    if flush and straight:
        print('Straight Flush')
        return 8
    elif quads:
        print('Four of a Kind')
        return 7
    elif trips and (pair_one or pair_two): 
        print('Full House')
        return 6
    elif flush:
        print('Flush')
        return 5
    elif straight:
        print('Straight')
        return 4
    elif trips:
        print('Three of a Kind')
        return 3
    elif pair_one and pair_two:
        print('Two Pair')
        return 2
    elif pair_one or pair_two:
        print('Pair')
        return 1
    else:
        print('High Card: ' + str(value))
        return 0

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

while eval != 9:
    count += 1

    for i in range(7):
        test_deck.shuffle()
    test_hand = []
    for i in range(5):
        test_hand.append(test_deck.take_card())
    eval = evaluate_hand(test_hand)

print('...found after ' + str(count) + ' hands')


# notes
# you can take out the in play list, and just use deck or dealt.  It'll be simpler, there's no need to track in play seperately
# use a dictionary for player names and positions?
