from .hand import Hand
from blackkjack_globals import map_actions_to_globals



class Player():
    """
    The Player class keeps track of the high level objectives:
    - What "rules" they are playing by (when to hit or hold)
    - Are the bust?
    - Did they blackjack?
    """
    def __init__(self, ruleset=None, chips:int=0, min_wager:int=0):
        self.wager = min_wager
        self.hands = []
        self.chips = chips
        self.ruleset = ruleset

    def sum_first_deal(self):
        self.hands.append(Hand(self.wager))
        for hand_index in range(len(self.hands)):
            hand = self.hands[hand_index]
            hand.sum_first_deal()

    def clean_hand(self):
        self.hands = None

    def __reformat_dealer_hand(self, dealer_upcard):
        tens = ['J', 'Q', 'K']
        if dealer_upcard in tens:
            return '10'
        else:
            return dealer_upcard

    def action(self, hand_total, dealer_upcard):
        dealer_upcard = self.__reformat_dealer_hand(dealer_upcard)
        ruleset_action = self.ruleset.get_action_from_ruleset(hand_total, dealer_upcard)
        return map_actions_to_globals(ruleset_action)

    def get_dealer_action(self):
        #ONLY INTENDED FOR USE WITH DEALER OBJECT CLASS
        # returns the blackjack_globals action the dealer will take
        return self.ruleset(self.hands)