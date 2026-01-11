
from blackkjack_globals import *


def get_dealer_hits_soft_17_hand_total(dealer_hands):
    #Only intended for dealer class
    assert len(dealer_hands) == 1, "Not being used in Dealer class"
    hand = dealer_hands[0]
    values = [c.value for c in hand.cards]

    # Sum non-ace values and count aces
    non_ace_total = 0
    ace_count = 0
    for v in values:
        if v == 'A':
            ace_count += 1
        else:
            non_ace_total += int(CARD_VALUES[v])

    # Compute best total: start with all aces as 11, then convert as needed
    total = non_ace_total + ace_count * 11
    converted_aces = 0
    while total > 21 and ace_count - converted_aces > 0:
        total -= 10
        converted_aces += 1

    # soft_amount is True if at least one ace is currently being counted as 11
    soft_amount = (ace_count - converted_aces) > 0

    return total, soft_amount

def dealer_hits_soft_17_ruleset_action(hand_total, soft_hand):
    if hand_total < 17:
        return HIT
    elif hand_total == 17:
        if soft_hand:
            return HIT
        else:
            return STAY
    else:
        return STAY

def get_dhs17_ruleset_action(dealer_hands):
    hand_total, soft_amount = get_dealer_hits_soft_17_hand_total(dealer_hands)
    return dealer_hits_soft_17_ruleset_action(hand_total, soft_amount)