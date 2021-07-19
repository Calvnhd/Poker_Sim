import random

class Deck:
    def __init__(self):
        self.deck = []
        self.discard = []
        self.in_play = []
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
    def get_discard_size(self):
        return len(self.discard)
    def get_in_play_size(self):
        return len(self.in_play)
    def shuffle(self):
        shuffled = []
        if len(self.discard) > 0:
            self.deck.extend(self.discard)
            self.discard = []
        if len(self.in_play) > 0:
            self.deck.extend(self.in_play)
            self.in_play = []
        for card in range(len(self.deck)):
            shuffled.append(self.deck.pop(random.randint(0, len(self.deck)-1)))
        self.deck = shuffled[:]
        if len(self.deck) != 52:
            print("WARNING: something has gone wrong with your shuffling") # Figure out how to throw proper error messages and update this
    def add_discard(self, card):
        self.discard.append(card)
    def take_card(self, is_discard):
        card = self.deck.pop(0)
        if is_discard:
            self.discard.append(card)
        else:
            self.in_play.append(card)
        return card
    def list_deck(self):
        print(self.deck)
    def list_discard(self):
        print(self.discard)
    def list_in_play(self):
        print(self.in_play)
    def info(self):
        print('Number of cards...')
        print('In play: ' + str(len(self.in_play)))
        print('Discarded: ' + str(len(self.discard)))
        print('Remaining: ' + str(len(self.deck)))

def evaluate_hand(hand):
    quads = False
    trips = False
    pair_one = False
    pair_two = False
    flush = False
    straight = False

    ranks = set()    
    suits = set()
    for i in range(len(hand)):
        ranks.add(hand[i][0])
        suits.add(hand[i][1])
    ranks_sorted = sorted(ranks)

    print(hand)

# check for flush
    if len(suits) == 1:
        flush = True
# check for straight
    if len(ranks) == 5:
        # this seems too brute?
        if ranks_sorted[4] == 14 and ranks_sorted[3] == 5: # Ace is low
            ranks_sorted[4] == 1
            ranks_sorted = sorted(ranks_sorted)
        if ((ranks_sorted[0] + 1) == ranks_sorted[1]) and ((ranks_sorted[1] + 1) == ranks_sorted[2]) and ((ranks_sorted[2] + 1) == ranks_sorted[3]) and ((ranks_sorted[3] + 1) == ranks_sorted[4]):
            straight = True
    elif len(ranks) == 4: # check for quads, trips, pairs
        pair_one = True
    elif len(ranks) == 3:
        pass
    else:
        pass
#1 2 3 4 5 -- set of 5 -- high card DONE
#1 1 2 3 4 -- set of 4 -- one pair
#1 1 2 2 3 -- set of 3 -- two pair
#1 1 1 2 3 -- set of 3 -- 3 of a kind
#1 1 1 2 2 -- set of 2 -- full house
#1 1 1 1 2 -- set of 2 -- quads

# find highest card

# check for kickers
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
        #print('High Card')
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

# INTERACTIVE INPUTS CAN COME LATER
#print("\n ===== Welcome to Calvin's Poker Simulator! =====")
#deck = Deck()
#deck.shuffle()
#player_count = int(input('\nEnter number of players: '))
#while player_count != 3:
#    print('This poker sim is currently limited to 3 players')
#    print('Please enter 3')
#    print("I know it's silly to ask. This will be updated eventually, I promise :)")
 #   player_count = int(input('Enter number of players: '))
#starting_stack = int(input('Enter starting chip stack: '))
#while starting_stack < 100 or starting_stack > 300:    
#    print('Starting stack must be between 100 and 300 chips')
#    starting_stack = int(input('Enter starting chip stack: '))
#bb = int(input('Enter Big Blind: '))
#while bb < 2 or bb > 10:
#    print('Big Blind must be between 1 and 10 chips')
#    bb = int(input('Enter Big Blind: '))
#sb = bb /2

# Update this with a for loop to have a flexible number of players (3 to 8)
#p1 = Player(input('Player 1 name: '), starting_stack, 0)
#p2 = Player(input('Player 2 name: '), starting_stack, 1)
#p3 = Player(input('Player 3 name: '), starting_stack, 2)

#print('\n===== Set-up complete! =====\n')

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
def game_details():
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
    players[i].give_card(deck.take_card(False))
for i in range(player_count):
    players[i].give_card(deck.take_card(False))

pot += players[1].bet(sb)
pot += players[2].bet(bb)

# Flop
deck.take_card(True) #Burn
board.append(deck.take_card(False))
board.append(deck.take_card(False))
board.append(deck.take_card(False))

# Turn
deck.take_card(True) #Burn
board.append(deck.take_card(False))

# River
deck.take_card(True) #Burn
board.append(deck.take_card(False))

# for testing hand eval
eval = -1
count = 0
test_deck = Deck()
test_hand = []
straight_ace = False

while eval != 5:
    count += 1

    for i in range(7):
        test_deck.shuffle()
    test_hand = []
    for i in range(5):
        test_hand.append(test_deck.take_card(False))
    eval = evaluate_hand(test_hand)

print('...found after ' + str(count) + ' hands')


# notes
# you can take out the in play list, and just use deck or dealt.  It'll be simpler, there's no need to track in play seperately
# use a dictionary for player names and positions?
