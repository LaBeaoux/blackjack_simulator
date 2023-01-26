
STAY = 0
HIT = 1
DOUBLE_DOWN = 2
SPLIT = 3
DOUBLE_DOWN_ELSE_SURRENDER = 4
SURRENDER = 5

HAND_TOTALS = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
               '10': 10, '11': 11, '12': 12, '13': 13, '14': 14, '15': 15, '16': 16,
               '17': 17, '18': 18, '19': 19, '20': 20, '21': 21,
               'A2': 13, 'A3': 14, 'A4': 15, 'A5': 16, 'A6': 17, 'A7': 18, 'A8': 19, 'A9': 20, 'A10': 21,
               'A11': 12, 'A12': 13, 'A13': 14, 'A14': 15, 'A15': 16, 'A16': 16, 
               'A17': 18, 'A18': 19, 'A19': 20, 'A20': 21,
               'AA': 2, '22': 4, '33': 6, '44': 8, '55': 10, '66': 12, '77': 14,
               '88':16, '99': 18, 'TT': 20, 'JJ': 20, 'QQ': 20, 'KK':20}

CARD_VALUES = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6':6,
               '7': 7, '8': 8, '9': 9, '10': 10,
               'J': 10, 'Q':10, 'K':10}
SUITS = ['D', 'S', 'C', 'H']
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

RULESET_INDICES = {'5': 0, '6': 1, '7': 2, '8': 3, '9': 4,
                   '10': 5, '11': 6, '12': 7, '13': 8, '14': 9,
                   '15': 10, '16': 11, '17': 12, '18': 13, '19': 14,
                   '20': 15, '21': 16, 
                   'A2': 17, 'A3': 18, 'A4': 19, 'A5': 20, 'A6': 21,
                   'A7': 22, 'A8': 23, 'A9': 24, 'A10': 25, 'A11': 26,
                   'AA': 27, '22': 28, '33': 29, '44': 30, '55': 31,
                   '66': 32, '77': 33, '88': 34, '99': 35, 'TT': 26
                   }

def map_actions_to_globals(action):
    if action == 'H':
        return HIT
    elif action == 'D':
        return DOUBLE_DOWN
    elif action == 'S':
        return STAY
    elif action == 'R':
        return SURRENDER
    elif action == 'P':
        return SPLIT
    else:
        return action

def lookup_hand_totals_map(hand):
    return HAND_TOTALS[hand]

def get_integer_totals(dealer_hand, player_hand):

    formatted_dealer_hand = dealer_hand.get_formatted_hand_total()
    formatted_player_hand = player_hand.get_formatted_hand_total()

    if 'A' in formatted_dealer_hand or 'T' in formatted_dealer_hand:
        dealer_total = lookup_hand_totals_map(formatted_dealer_hand)
    else:
        dealer_total = int(formatted_dealer_hand)

    if 'A' in formatted_player_hand or 'T' in formatted_player_hand:
        player_total = lookup_hand_totals_map(formatted_player_hand)
    else:
        player_total = int(formatted_player_hand)

    return dealer_total, player_total