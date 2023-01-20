
from blackkjack_globals import *


def get_dealer_hits_soft_17_hand_total(dealer_hands):
    #Only intended for dealer class
    assert len(dealer_hands) == 1, "Not being used in Dealer class"

    hand = dealer_hands[0]
    values = [cards.value for cards in hand.cards]
    soft_amount = False

    if 'A' in values:
        """
        If an Ace is in the hand need to consider soft-values
        Dealer will stay if either soft total is  [18 < total <= 21] so return this value if true
        Else dealer will hit
        """
        soft_amount = True
        amount = 0
        for value in values:
            if value != 'A':
                amount += int(CARD_VALUES[value])

        if ((amount >= 7) and (amount <= 10)):
            #This means Ace is 11
            hand_total = amount + 11
        elif ((amount >= 17) and (amount <= 20)):
            #This means Ace must be 1
            hand_total = amount + 1
        else:
            # If neither STAY criteria is met, just return the lower since the dealer will HIT regardless
            hand_total = amount + 1

    else:
        #If Ace not in hand, just count and add
        int_values = [CARD_VALUES[value] for value in values]
        hand_total = sum(int_values)
    
    return hand_total, soft_amount

def dealer_hits_soft_17_ruleset_action(hand_total, soft_hand):
    if hand_total <= 16:
        return HIT
    elif hand_total  == 17:
        if soft_hand:
            return HIT
        else:
            return STAY
    elif hand_total > 17:
        return STAY

def get_dhs17_ruleset_action(dealer_hands):
    hand_total, soft_amount = get_dealer_hits_soft_17_hand_total(dealer_hands)
    action = dealer_hits_soft_17_ruleset_action(hand_total, soft_amount)
    return action