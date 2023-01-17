from blackkjack_globals import *


class Card():
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    
    def get_value(self):
        if self.value == 'A':
            return [1, 11]
        else:
            return [CARD_VALUES[self.value]]