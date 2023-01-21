import unittest
import sys

from templates.hand import Hand

sys.path.append("/Users/aaronlabomascus/Projects/blackjack")

class TestFormattedHandTotal(unittest.TestCase):

    def get_formatted_hand_total(self):
        hand = Hand()
        
        #test_hand list structure
        #[CardA, CardB, ..., Expected str]
        test_values = [
            ['J', 'A', 'A11'],
            ['2', '3', '5'],
            ['2', '3', '4', '9'],
            ['K', 'Q', 'J', '30'],
            ['A', 'A', 'AA'],
            ['5', '5', '55'],
            ['5', '5', '5', '15'],
            ['7', 'A', 'A7'],
            ['J', '10', 'TT'],
            ['J', 'J', 'TT'],
            ['2', '3', '2', '4', '6', 'A', '19']
        ]

        test_hands = []
        for testcase in test_values:
            case = []
            case.append(testcase[-1])
            for value in testcase:
                case.insert(0, Card(value)) #Add to front of hand so expected value at end

        #build test hand
        for case in test_hands:
            expected_value = case.pop(-1)

            for card in case:
                hand.cards.append(card)

            print(f"{expected_value}")
            self.assertEqual(hand.get_formatted_hand_total(), expected_value, 
                             "formatted hand string not equal")
