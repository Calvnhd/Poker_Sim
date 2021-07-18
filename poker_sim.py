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
    
