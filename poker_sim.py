import random

class Deck:
    def __init__(self):
        self.is_shuffled = False
        self.deck = []
        self.discard = []
        for card in range(2,12):
            if card < 11:
                self.deck.append(str(card) + 'c')
                self.deck.append(str(card) + 's')
                self.deck.append(str(card) + 'h')
                self.deck.append(str(card) + 'd')
            else:
                self.deck.extend(['Jc','Js','Jh','Jd'])
                self.deck.extend(['Qc','Qs','Qh','Qd'])
                self.deck.extend(['Kc','Ks','Kh','Kd'])
                self.deck.extend(['Ac','As','Ah','Ad'])
    def get_size(self):
        return len(self.deck)
    def get_discard_size(self):
        return len(self.discard)
    def shuffle(self):
        shuffled = []
        if len(self.discard) > 0:
            self.deck.extend(self.discard)
        for card in range(len(self.deck)):
            shuffled.append(self.deck.pop(random.randint(0, len(self.deck)-1)))
        self.deck = shuffled[:]
        self.is_shuffled = True
    def shuffle_check(self):
        return self.is_shuffled
    def add_discard(self, card):
        self.discard.append(card)
    def take_card(self):
        return self.deck.pop(0)
    def list_deck(self):
        print(self.deck)
    def list_discard(self):
        print(self.discard)
    
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
        print('Name:     ' + str(self.name))
        print('Chips:    ' + str(self.chips))
        print('Hand      ' + str(self.hand))
        print('Position: ' + str(self.position))
    def set_position(self, position):
        self.position = position
    
print("\n ===== Welcome to Calvin's Poker Simulator! =====")
deck = Deck()
deck.shuffle()
player_count = int(input('\nEnter number of players: '))
while player_count != 3:
    print('This poker sim is currently limited to 3 players')
    print('Please enter 3')
    print("I know it's silly to ask. This will be updated eventually, I promise :)")
    player_count = int(input('Enter number of players: '))
starting_stack = int(input('Enter starting chip stack: '))
while starting_stack < 100 or starting_stack > 300:    
    print('Starting stack must be between 100 and 300 chips')
    starting_stack = int(input('Enter starting chip stack: '))
bb = int(input('Enter Big Blind: '))
while bb < 1 or bb > 10:
    print('Big Blind must be between 1 and 10 chips')
    bb = int(input('Enter Big Blind: '))
sb = bb /2

p1 = Player(input('Player 1 name: '), starting_stack, 0)
p2 = Player(input('Player 2 name: '), starting_stack, 1)
p3 = Player(input('Player 3 name: '), starting_stack, 2)

print('\n===== Set-up complete! =====\n')

def game_details():
    print('\n===  GAME DETAILS ===')
    print(str(player_count) + 'Players\n')
    p1.get_info()
    p2.get_info()
    p3.get_info()

