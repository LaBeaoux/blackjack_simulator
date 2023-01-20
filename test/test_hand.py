import unittest

from templates.hand import Hand
from templates.card import Card



class TestFormattedHandTotal(unittest.TestCase):

    def get_formatted_hand_total(self):
        hand = Hand()
        
        #test_hand list structure
        #[CardA, CardB, ..., Expected str]
        test_hands = [
            [Card('J'), Card('A'), 'A11']
        ]

        #build test hand
        for case in test_hands:
            expected_value = case.pop(-1)

            for card in case:
                hand.cards.append(card)

            self.assertEqual(hand.get_formatted_hand_total(), expected_value, 
                             "formatted hand string not equal")
