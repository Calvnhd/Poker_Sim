import cards

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
        max_bet = self.chips + my_prev_bet
        chips_left = self.chips
        print('max_bet set to: ' + str(max_bet))
        print('chips_left set to: ' + str(chips_left))


        if self.active == False:
            print('(PL) Inactive player. No action taken by ' + str(self.name))
            return [0,0]
        else: 
            if round == 0: # Pre-Flop
                p = 'Checking starting hand strength for ' + str(self.hand)
                val = start_hand_value(self.hand)
                p += ' ... Hand value: ' + str(val)
                print(p)
                # print('There are still ' + str(waits) + ' players left to take first action')
                if my_prev_bet == current_bet and (my_prev_bet !=0 or waits == 0):
                    # print('EVERYONE HAS EITHER CALLED OR FOLDED TO THIS PLAYER')
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
                    if ceiling > chips_left:
                        ceiling = chips_left
                    if target > chips_left:
                        target = chips_left
                    if current_bet > ceiling:
                        action = 'fold'
                        amount = my_prev_bet
                        self.best_hand = [0,0,0]
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
                    # print('EVERYONE HAS EITHER CALLED OR FOLDED TO THIS PLAYER')
                    action = 'end'
                    amount = my_prev_bet
                else:
                    # Determine hand strength and potential to hit/improve
                    # print('Checking Flop hand strength... ')
                    p = 'Current hand: ' + str(self.best_hand) + ' --- ' + str(cards.interpret_eval(self.best_hand))
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
                    if ceiling > chips_left:
                        ceiling = chips_left
                    if target > chips_left:
                        target = chips_left    
                    if current_bet > ceiling:
                        action = 'fold'
                        amount = my_prev_bet
                        self.active = False
                        self.best_hand = [0,0,0]
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
                    # print('EVERYONE HAS EITHER CALLED OR FOLDED TO THIS PLAYER')
                    action = 'end'
                    amount = my_prev_bet
                else:
                    # Determine hand strength and potential to hit/improve
                    # print('Checking Turn hand strength... ')
                    p = 'Current hand: ' + str(self.best_hand) + ' --- ' + str(cards.interpret_eval(self.best_hand))
                    outs = self.count_outs(board, round)
                    p += ' --- [goal,outs] for player ' + str(self.name) + ': ' + str(outs)
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
                    if ceiling > chips_left:
                        ceiling = chips_left
                    if target > chips_left:
                        target = chips_left
                    if current_bet > ceiling:
                        action = 'fold'
                        amount = my_prev_bet
                        self.active = False
                        self.best_hand = [0,0,0]
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
                if my_prev_bet == current_bet and (my_prev_bet !=0 or waits == 0):
                    action = 'end'
                    amount = my_prev_bet
                else:
                    # Determine hand strength and potential to hit/improve
                    print('Final hand: ' + str(self.best_hand) + ' --- ' + str(cards.interpret_eval(self.best_hand)))
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
                    if ceiling > chips_left:
                        ceiling = chips_left
                    if target > chips_left:
                        target = chips_left
                    if current_bet > ceiling:
                        action = 'fold'
                        amount = my_prev_bet
                        self.active = False
                        self.best_hand = [0,0,0]
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
        if amount < 0:
            print('ERROR! Betting negative chips')
        if (amount - my_prev_bet) < 0:
            print('ERROR! adding imaginary chips?')
        self.chips -= (amount-my_prev_bet)
        print('Ceiling: ' + str(ceiling) + '   Target: ' + str(target) + '   Amount (round cum.): ' + str(amount)+ '   Amount (this turn): ' + str(amount-my_prev_bet)  + '   Chips left: ' + str(self.chips))
        return [action,amount]

    def set_active(self, a):
        # print('Setting ' + self.name + ' active to ' + str(a) )
        self.active = a
    def is_active(self):
        return self.active
    def find_best_hand(self, board):
        self.best_hand = cards.make_hands(self.hand, board)
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
            
            # Goal reference: 0 - High Card, 1 - Pair, 2 - Two Pair, 3 - Trips, 4 - Straight, 5 - Flush, 6 - Full House, 7 - Quads, 8 - Straight Flush, 9 - Royal Flush 
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

        return [goal, outs]

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
