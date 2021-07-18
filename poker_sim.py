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
    
deck = Deck()
print(deck.get_size())
deck.list_deck()
deck.shuffle()
deck.list_deck()
print(deck.get_size())