import random
from typing import Sequence

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
        print('ERROR COMPARING HANDS for hand: ' + str(hand))
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
    if hand == [0,0,0]:
        return 'FOLDED'
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
    # print('COMPARING HANDS for h1 and h2: ' + str(h1) + ' ... ' + str(h2))
    # print('i: ' + str(i))
    if i == 7: # Base case
        print('ERROR COMPARING HANDS for h1 and h2: ' + str(h1) + ' ... ' + str(h2) + ' ... i == 7')
        return -1
    if h1 == h2:
        # print('h1 == h2: ' + str(h1) + ' == ' + str(h2))
        return 0
    if h1[i] > h2[i]:
        # print('h1[i] > h2:[i] ' + str(h1[i]) + ' > ' + str(h2[i]))
        return h1
    elif h1[i] < h2[i]:
        # print('h1[i] < h2:[i] ' + str(h1[i]) + ' == ' + str(h2[i]))
        return h2
    else:
        if h1[i] == h2[i] and len(h1) == len(h2):
            # print('h1[i] and h2[i] are equal. h1 and h2 are equal length')
            i += 1
            return compare_hands(h1,h2,i)
        if h1 == [0,0,0] and h2 != [0,0,0]:
            # print('h1 is folded')
            return h2
        if h2 == [0,0,0] and h1 != [0,0,0]:
            # print('h2 is folded')
            return h1
        else:
            print('ERROR COMPARING HANDS for h1 and h2: ' + str(h1) + ' ... ' + str(h2))
            return -1

# Finds the best hand a player can make with their 2 cards
# takes 2 cards from hand, 3 to 5 cards from board, and returns the best hand in the form of eval code
def make_hands(H, B):
    if len(H) + len(B) < 5:
        print('ERROR! Not enough cards on board to make_hands')
        return -1

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

# Determines the value of a starting 2 card hand [[r,s][r,s]]
# Returns a rating from 0 (worst) to 15 (best)
# move this into Player object?
def start_hand_value(h):
    pockets = False
    suited = False
    connectors = False
    straight_range = False
    both_high = False
    one_high = False

    r1 = h[0][0]
    r2 = h[1][0]
    s1 = h[0][1] 
    s2 = h[1][1]

    msg = ''
    if s1 == s2:
        msg += 'SUITED '
        suited = True
    if r1 == r2:
        pockets = True
        msg += 'POCKETS '
    elif abs(r1 - r2) == 1:
        msg += 'CONNECTORS '
        connectors = True
    elif abs(r1 - r2) <= 4:
        msg += 'STRAIGHT RANGE '
        straight_range = True
    if r1 > 9 or r2 > 9:
        msg += 'ONE HIGH '
        one_high = True
    if r1 > 9 and r2 > 9:
        msg += 'BOTH HIGH '
        both_high = True
    if (r1 == 14 or r2 == 14) and (r1 <= 5 or r2 <= 5):
        msg += 'STRAIGHT RANGE '
        straight_range = True

    # print(msg)

    if both_high:
        if pockets:
            return 15
        if suited:
            if connectors:
                return 14
            if straight_range:
                return 13
        if connectors:
            return 12
        if straight_range: # Always true for cards both_high (>=10)
            return 11
        else:
            return 10 # not currently possible.  Leave in case 'high' threshold lowers below 10.
    elif pockets:
        return 10
    elif one_high:
        if suited:
            if connectors: # 9 10 suited only (Rare)
                return 9
            if straight_range:
                return 8
        if connectors:
            return 7
        if straight_range:
            return 6
        else:
            return 3
    else: 
        if suited:
            if connectors:
                return 5
            if straight_range: 
                return 4
        if connectors:
            return 2
        if straight_range:
            return 1
        else: 
            return 0

# returns bool for flush draw
# input hand[] and/or board[], combined total of 4 to 6 cards
def is_f_draw(h,b=[]): 
    seen = h[:]
    seen.extend(b)
    f_draw = False
    if len(seen) > 3 and len(seen) < 7:
        # extract suits
        suits = []
        for i in range(len(seen)):
            suits.append(seen[i][1])
        s = list(set(suits))

        for i in range(len(s)):
            count = 0
            for j in range(len(suits)):
                if s[i] == suits[j]:
                    count += 1
            if count == 4:
                f_draw = True
    else:
        print('ERROR: Too many cards to calculate Flush draw') 
    return f_draw

# returns Straight draw bool [True = draw, True = open]
# input hand[] and/or board[], combined total of 4 to 6 cards
def is_s_draw(h,b=[]): # returns bool for [True = draw, True = open]
    cards = h[:]
    cards.extend(b)
    ranks = []
    has_ace = False

    if len(cards) > 3 and len(cards) < 7: # must input 4 5 or 6 cards
        # get ranks
        for i in range(len(cards)):
            ranks.append(cards[i][0])
            if cards[i][0] == 14:
                has_ace = True
        ranks.sort()
    
        # print('\nranks: '+str(ranks))
        for i in range(len(ranks)-3):
            # make a subset of 4
            r = []
            for j in range(4):
                r.append(ranks[j+i])
            # print('    r: ' + str(r))
            # find a run of four
            if r[0]+1 == r[1]:
                if r[0]+2 == r[2]:
                    if r[0]+3 == r[3]:
                        # print('4 consecutive numbers')
                        if has_ace == True:
                            # print('Straight draw, Ace high')
                            return [True, False]
                        else:
                            # print('Open straight draw')
                            return [True, True]
            # test other consecutive / gap combinations
            if (r[3] - r[0]) == 4: # in Straight range
                if r[0]+2 == r[1] and r[0]+3 == r[2]:
                    # print('ACDE: Inside Straight Draw')
                    return [True, False]
                if r[0]+1 == r[1] and r[0]+3 == r[2]:
                    # print('ABDE: Inside Straight Draw')
                    return [True, False]
                if r[0]+1 == r[1] and r[0]+2 == r[2]:
                    # print('ABCE: Inside Straight Draw')
                    return [True, False]

        if has_ace == True: # repeat the process once more with ace low
            # print('Consider ace low...')
            ranks = []
            for i in range(len(cards)):
                if cards[i][0] == 14:
                    ranks.append(1) # convert ace to low
                else:
                    ranks.append(cards[i][0])
            ranks.sort()

            # make a subset of 4 only need first 4 to test low ace scenario
            r = []
            for j in range(4):
                r.append(ranks[j])
            # find a run of four
            if r[0]+1 == r[1]:
                if r[0]+2 == r[2]:
                    if r[0]+3 == r[3]:
                        # print('4 consecutive numbers.')
                        # print('Straight draw, Ace low')
                        return [True, False]
            # test other consecutive / gap combinations
            if (r[3] - r[0]) == 4:  # in Straight range
                if r[0]+2 == r[1] and r[0]+3 == r[2]:
                    # print('ACDE: Inside Straight Draw')
                    return [True, False]
                if r[0]+1 == r[1] and r[0]+3 == r[2]:
                    # print('ABDE: Inside Straight Draw')
                    return [True, False]
                if r[0]+1 == r[1] and r[0]+2 == r[2]:
                    # print('ABCE: Inside Straight Draw')
                    return [True, False]
    else:
        print('ERROR: Straight Draw input must be 4, 5, or 6 cards')
    return [False, False]

# Expand using inheritance to add different player archetypes
class Player:
    def __init__(self, name, chips, position):
        self.name = name
        self.chips = chips
        self.hand = []
        self.position = position
        self.best_hand = []
        self.active = True
    def get_chips(self):
        return self.chips
    def bet(self, amount):
        if self.chips >= amount:
            self.chips -= amount
            return amount
        else: # bet all remaining chips
            chips_left = self.chips
            self.chips = 0
            return chips_left
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
    def get_best_hand(self):
        if self.best_hand == []:
            print('ERROR!  Best hand not set for player name ' + str(self.name) + '. Setting folded [0,0,0] hand as best hand')
            return [0,0,0]
        return self.best_hand
    def set_best_hand(self, h):
        self.best_hand = h

    # return decision
    # [fold/call/bet or raise , amount]
    def action(self, round, board, pot, bb, current_bet, prev_raise, my_prev_bet, waits): # Decide whether to bet/raise or call (return int amount), or check/fold (return 0)
        print(str(self.name + ' in position ' + str(self.position)))
        p_info = '*** '
        p_info += 'pl remaining chips: ' + str(self.chips) + ' --- '
        p_info += 'pl cumulative bets: ' + str(my_prev_bet)+ ' --- '
        p_info += 'round: ' + str(round)+ ' --- '
        p_info += 'pot: ' + str(pot)+ ' --- '
        p_info += 'current_bet: ' + str(current_bet)+ ' --- '
        p_info += 'prev_raise: ' + str(prev_raise)+ ' ***'
        print(p_info)

        amount = 0
        ceiling = 0
        target = 0
        action = ''
        max_bet = self.chips

        if self.active == False:
            print('(PL) Inactive player. No action taken by ' + str(self.name))
        else: 
            if round == 0: # Pre-Flop
                p = 'Checking starting hand strength for... ' + str(self.hand)
                val = start_hand_value(self.hand)
                p += ' ... Hand value: ' + str(val)
                print(p)
                # print('There are still ' + str(waits) + ' players left to take first action')
                if my_prev_bet == current_bet and (my_prev_bet !=0 or waits == 0):
                    print('EVERYONE HAS EITHER CALLED OR FOLDED TO THIS PLAYER')
                    action = 'end'
                    amount = my_prev_bet
                else:
                    if val >=10:
                        ceiling = 10*bb
                        target = 5*bb
                    elif val >=2:
                        ceiling = 5*bb
                        target = 2*bb
                    else:
                        ceiling = 0
                        target = 0
                    if current_bet > ceiling:
                        action = 'fold'
                        amount = my_prev_bet
                        self.active = False
                    elif current_bet >= 0 and current_bet <= ceiling and (current_bet + prev_raise) >= (target + bb): 
                        action = 'call'
                        amount = current_bet
                    elif current_bet >= 0 and current_bet <= ceiling and (current_bet + prev_raise) <= ceiling: 
                        action = 'bet'
                        if (current_bet + prev_raise) < target:
                            amount = target
                        else:
                            amount = current_bet + prev_raise
                    elif current_bet <= ceiling:
                        action = 'call'
                        amount = current_bet
            elif round == 1: # Flop
                # print('There are still ' + str(waits) + ' players left to take first action')
                if my_prev_bet == current_bet and (my_prev_bet !=0 or waits == 0):
                    print('EVERYONE HAS EITHER CALLED OR FOLDED TO THIS PLAYER')
                    action = 'end'
                    amount = my_prev_bet
                else:
                    # Determine hand strength and potential to hit/improve
                    print('Checking Flop hand strength... ')
                    p = 'Current hand: ' + str(self.best_hand) + ' --- ' + str(interpret_eval(self.best_hand))
                    outs = self.count_outs(board, round)
                    p += ' --- outs for player ' + str(self.name) + ': ' + str(outs)
                    print(p)
                    if self.best_hand[0] > 4:
                        ceiling = max_bet
                        target = 20*bb
                    elif self.best_hand[0] > 0 or outs[0] >=3:
                        ceiling = 20*bb
                        target = 5*bb
                    else:
                        ceiling = 0
                        target = 0
                    if current_bet > ceiling:
                        action = 'fold'
                        amount = my_prev_bet
                        self.active = False
                    elif current_bet >= 0 and current_bet <= ceiling and (current_bet + prev_raise) >= (target + bb): 
                        action = 'call'
                        amount = current_bet
                    elif current_bet >= 0 and current_bet <= ceiling and (current_bet + prev_raise) <= ceiling: 
                        action = 'bet'
                        if (current_bet + prev_raise) < target:
                            amount = target
                        else:
                            amount = current_bet + prev_raise
                    elif current_bet <= ceiling:
                        action = 'call'
                        amount = current_bet
            elif round == 2: # Turn
                # print('There are still ' + str(waits) + ' players left to take first action')
                if my_prev_bet == current_bet and (my_prev_bet !=0 or waits == 0):
                    print('EVERYONE HAS EITHER CALLED OR FOLDED TO THIS PLAYER')
                    action = 'end'
                    amount = my_prev_bet
                else:
                    # Determine hand strength and potential to hit/improve
                    print('Checking Turn hand strength... ')
                    p = 'Current hand: ' + str(self.best_hand) + ' --- ' + str(interpret_eval(self.best_hand))
                    outs = self.count_outs(board, round)
                    p += ' --- outs for player ' + str(self.name) + ': ' + str(outs)
                    print(p)
                    if self.best_hand[0] > 4:
                        ceiling = max_bet
                        target = 20*bb
                    elif self.best_hand[0] > 0 or outs[0] >=3:
                        ceiling = 20*bb
                        target = 5*bb
                    else:
                        ceiling = 0
                        target = 0
                    if current_bet > ceiling:
                        action = 'fold'
                        amount = my_prev_bet
                        self.active = False
                    elif current_bet >= 0 and current_bet <= ceiling and (current_bet + prev_raise) >= (target + bb): 
                        action = 'call'
                        amount = current_bet
                    elif current_bet >= 0 and current_bet <= ceiling and (current_bet + prev_raise) <= ceiling: 
                        action = 'bet'
                        if (current_bet + prev_raise) < target:
                            amount = target
                        else:
                            amount = current_bet + prev_raise
                    elif current_bet <= ceiling:
                        action = 'call'
                        amount = current_bet
            elif round == 3: # River
                # print('There are still ' + str(waits) + ' players left to take first action')
                if my_prev_bet == current_bet and (my_prev_bet !=0 or waits == 0):
                    print('EVERYONE HAS EITHER CALLED OR FOLDED TO THIS PLAYER')
                    action = 'end'
                    amount = my_prev_bet
                else:
                    # Determine hand strength and potential to hit/improve
                    print('Checking River hand strength... ')
                    print('Final hand: ' + str(self.best_hand) + ' --- ' + str(interpret_eval(self.best_hand)))
                    if self.best_hand[0] > 5:
                        ceiling = max_bet
                        target = max_bet
                    elif self.best_hand[0] > 4:
                        ceiling = max_bet
                        target = 20*bb
                    elif self.best_hand[0] > 0:
                        ceiling = 5*bb
                        target = bb
                    else:
                        ceiling = 0
                        target = 0
                    if current_bet > ceiling:
                        action = 'fold'
                        amount = my_prev_bet
                        self.active = False
                    elif current_bet >= 0 and current_bet <= ceiling and (current_bet + prev_raise) >= (target + bb): 
                        action = 'call'
                        amount = current_bet
                    elif current_bet >= 0 and current_bet <= ceiling and (current_bet + prev_raise) <= ceiling: 
                        action = 'bet'
                        if (current_bet + prev_raise) < target:
                            amount = target
                        else:
                            amount = current_bet + prev_raise
                    elif current_bet <= ceiling:
                        action = 'call'
                        amount = current_bet
        # to ensure max bet isn't exceeded when target < chips left
        if amount > max_bet:
            amount = max_bet
        self.chips -= (amount-my_prev_bet)
        print('Ceiling: ' + str(ceiling) + '   Target: ' + str(target) + '   Chips left: ' + str(self.chips) + '   Amount: ' + str(amount) )        
        return [action,amount]

    def set_active(self, a):
        print('Setting ' + self.name + ' active to ' + str(a) )
        self.active = a
    def is_active(self):
        return self.active
    def find_best_hand(self, board):
        self.best_hand = make_hands(self.hand, board)
    # returns list [goal,outs]
    # goal: best case hand improvement, outs: number of cards (chances) to hit goal
    def count_outs(self, board, round):
        self.find_best_hand(board)
        # print(str(self.best_hand) + ' --- ' + str(interpret_eval(self.best_hand)))
        outs = 0 
        goal = 0 
        s_draw = is_s_draw(self.hand, board)
        f_draw = is_f_draw(self.hand, board)

        # https://redsharkpoker.com/poker-outs/ for info on outs calculations
        if round == 0: # Pre-Flop
            print('ERROR: Still Pre-Flop')
        elif round == 1 or round == 2: # Flop or Turn
            if s_draw[0] == True and s_draw[1] == True and f_draw == True: # Open SF sraw
                outs = 15
                goal = 8 # SF best, Straight (4) or Flush (5) possible
            elif s_draw[0] == True and s_draw[1] == False and f_draw == True: # Inside SF draw
                outs = 12
                goal = 8 # SF best, Straight (4) or Flush (5) possible
            else:
                if s_draw[0] == True and f_draw == False and self.best_hand[0] < 4: # Straight draw
                    if s_draw[1] == True: # open s draw
                        outs = 8
                    else: # inside s draw
                        outs = 4
                    goal = 4
                elif f_draw == True and self.best_hand[0] < 5:
                    outs = 9
                    goal = 5
            
            if goal == 0 and self.best_hand[0] < 7: 
                if self.best_hand[0] == 0: # High card
                    outs = 6 # (Pair)
                    goal = 1
                elif self.best_hand[0] == 1: # Pair
                    outs = 5 # 2 (Trips) + 3 (Two Pair)
                    goal = 3
                elif self.best_hand[0] == 2: # Two Pair
                    outs = 4 # (Full House)
                    goal = 6
                elif self.best_hand[0] == 3: # Trips
                    outs = 7 # 1 (Quads) + 6 (Full House)
                    goal = 7
                elif self.best_hand[0] == 5: # Flush
                    if s_draw[0] == True:
                        if s_draw[1] == True: # Open SF draw
                            outs = 2
                        elif s_draw[1] == False: # Inside SF draw
                            outs = 1
                        goal = 8
                elif self.best_hand[0] == 6: # Full House
                    outs = 1 # to hit quads
                    goal = 7
            if goal == 0:
                goal = self.best_hand[0] # No improvement possible. Return current hand as goal.
                
        elif round == 3: # River
            print('All cards dealt. This is as good as it gets.')
            goal = self.best_hand[0]

        # if goal == 1:
        #     g = 'Pair'
        # elif goal == 2:
        #     g = 'Two Pair'
        # elif goal == 3:
        #     g = 'Trips'
        # elif goal == 4:
        #     g = 'Straight'
        # elif goal == 5:
        #     g = 'Flush'
        # elif goal == 6:
        #     g = 'Full House'
        # elif goal == 7:
        #     g = 'Quads'
        # elif goal == 8:
        #     g = 'Straight Flush'
        # print('Can improve to ' + g + ', outs found: ' + str(outs))

        return [goal, outs]

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
        print('Setting round to 0 in game.update_positions')
        self.round = 0
    def update_round(self): # increments round, or returns to zero for new deal
        if self.round == 3:
            self.round = 0
        else:
            self.round += 1
        print('Setting round to ' + str(self.round) + ' in game.update_round')
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
        if self.pot != 0 and self.round == 0:
            print('ERROR!  POT NOT TAKEN BEFORE NEXT DEAL')
            self.pot = 0
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
        self.pot = 0
        return output
    # adapt this to exclude inactive players from leaders[]
    def find_leaders(self): # creates list hands[] of best 5 card hand (in eval code) for each player, sets best_hand for player object, finds best_hand overall, and creates list leaders[] of player objects who hold the best hand 
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
            print('Looking for the best hand from each player...')
            self.hands = []
            for i in range(self.player_count):
                if self.players[i].is_active():  # exclude inactive players
                    self.hands.append(make_hands(self.players[i].get_hand(), self.board))
                    self.players[i].set_best_hand(self.hands[i])
                else:
                    self.hands.append([0,0,0]) # folded hand
                    self.players[i].set_best_hand([0,0,0])
                self.best_hand = find_best_hand(self.hands)
            print('Player hands: ' + str(self.hands))
            print('Best hand: ' + str(self.best_hand) + ' ... ' + str(interpret_eval(self.best_hand)))
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
    def hand_info(self):
        output = ''
        if len(self.board) >= 3:
            if self.player_count != len(self.hands):
                self.find_leaders()
            for i in range(self.player_count):
                output += (str(self.players[i].get_name()) + ': ' + interpret_eval(self.players[i].get_best_hand()) + '\n')
            output += ('Best hand: ' + str(interpret_eval(self.best_hand))) 
        else:
            output = "ERROR! CAN'T PRINT HAND INFO PRE-FLOP"
        return output
    def count_active_players(self):
        c = 0
        for i in range(self.player_count):
            if self.players[i].is_active() == True:
                c += 1
        return c
    # Return continue dealing or award pot (+ winner and amount) 
    def players_act(self):
        # initialize values
        end_name = 0
        player_bets = []  # track how many chips a player has committed per betting round
        player_turn_count = [] # track how many turns a player has taken.  Not sure if you need this??
        for i in range(self.player_count):
            player_bets.append(0)
            player_turn_count.append(0)
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
            # find sb and bb and add to player_bets[]
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
        # #
        print('First to act at position ' + str(player_turn))
        w = 0
        while done == False:
            print('----------------------------------------------------------    Loop: ' + str(w))
            print('LOOP SUMMARY')
            print('  Names: ' + str(names))
            print(' Active: ' + str(players_active))
            print('Actions: ' + str(player_actions))
            print('   Bets: ' + str(player_bets))
            print(' ')
        
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
                        print('Action: ' + str(action))
                        player_actions[i] = action[0]
                        player_bets[i] = action[1]
                        print(names)
                        print(player_actions)
                        print(player_bets)
                        if action[0] == 'fold':
                            players_active[i] = False
                        elif action[0] == 'end':
                            print('End action detected in Game loop at player ' + str(self.players[i].get_name()))
                            end_name = self.players[i].get_name()
                            done = True
                            break
                       

                        # update info for next player decision
                        if action[1] > 0: # bet or call
                            print('adding ' + str(action[1] - pl_prev_bet) + ' to the pot')
                            self.pot += (action[1] - pl_prev_bet) # add bet/call to pot
                            if action[1] > current_bet: # find raise
                                prev_raise = abs(action[1] - current_bet)
                                current_bet = action[1]

                    else:
                        print(str(self.players[i].get_name()) + ' is not active (GL)') 

                    if player_turn == self.player_count - 1:
                        player_turn = 0 
                    else: 
                        player_turn += 1
                    print('Next player to act is at position ' + str(player_turn) + '\n')
           
            # for testing / safety
            if w > 10: 
                print('While loop killed by w > condition')
                done = True
            # For testing
            w += 1
        
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
    def is_game_over(self):
        no_chips = 0
        for i in range(self.player_count):
            if self.players[i].get_chips() == 0:
                no_chips += 1
        if no_chips == self.player_count - 1:
            return True
        else:
            return False




game = Game(['CD', 'IK', 'BM'])
done = False
last_game = False

i = 0
while not done:
    print('\n***********************************  Game ' + str(i) + ' ***********************************')

    game.deal() # deal & blinds
    print(game.info())
    print('\nPre-Flop Actions ====================')
    results = game.players_act()
    print('=====================================')
    print('Pre-Flop results: ' + str(results))
    print('=====================================\n')
    game.update_round()

    print('Game sees ' + str(game.count_active_players()) + ' active players remaining before Flop')
    if game.count_active_players() > 1:
        game.deal() # flop
        print(game.info())
        print(game.hand_info())
        print('\nFlop Actions ========================')
        results = game.players_act()
        print('=====================================')
        print('Flop results: ' + str(results))
        print('=====================================\n')
        game.update_round()
        
        print('Game sees ' + str(game.count_active_players()) + ' active players remaining before Turn')
        if game.count_active_players() > 1:
            game.deal() # turn
            print(game.info())
            print(game.hand_info())
            print('\nTurn Actions ========================')
            results = game.players_act()
            print('=====================================')
            print('Turn results: ' + str(results))
            print('=====================================\n')
            game.update_round()

            print('Game sees ' + str(game.count_active_players()) + ' active players remaining before Turn')
            if game.count_active_players() > 1:
                game.deal() # river
                print(game.info())
                print(game.hand_info())
                print('\nRiver Actions =======================')
                results = game.players_act()
                print('=====================================')
                print('River results: ' + str(results))
                print('=====================================\n')
                game.update_round()

    print('\n***** END OF HAND *****')
    print('Game sees ' + str(game.count_active_players()) + ' active players at end')
    if game.count_active_players() > 1:
        print('SHOWDOWN!')
    game.find_leaders()
    print('... Awarding pot ...')
    print(game.award_pot())

    game.update_positions()
    if (game.is_game_over()):
        print('\n--- Only one player remaining.  Game over after ' + str(i) + ' hands ---')
        print(game.info())
        done = True

    i += 1

    ### for testing
    if i > 10000:
        print('\n--- loop killed by max i = ' + str(i) + ' ---')
        print(game.info())
        done = True

    

# # Core loop to date 27/7
# game = Game(['CD', 'IK', 'BM'])
# for i in range(1):
#     print('\n====  Game ' + str(i) + ' ====')
#     game.deal() # deal & blinds
#     game.update_round()
#     game.deal() # flop
#     game.update_round()
#     game.deal() # turn
#     game.update_round()
#     game.deal() # river
#     game.update_round()
#     game.find_leaders()
#     print(game.info())
#     print(game.hand_info())
#     print(game.award_pot())
#     game.update_positions()