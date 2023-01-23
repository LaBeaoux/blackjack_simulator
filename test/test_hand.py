import unittest
import sys

from templates.hand import Hand
from templates.card import Card

sys.path.append("/Users/aaronlabomascus/Projects/blackjack") #Necessary... Not sure why yet

"""
To run unittest class:
from commandline of project root, e.g. /Users/<user>/Projects/blackjack
 - run `python -m unittest test.test_hand`
Or to find and run all available unit tests
 - run `python -m unittest discover
There are also alternatives to specify specific test functions only
"""

class TestFormattedHandTotal(unittest.TestCase):

    def test_get_formatted_hand_total(self):
        test_values = [
            {'cards': ['J', 'A'],  'expected': 'A10', 'assert': 'equal'},
            {'cards': ['2', '3'],  'expected': '5',   'assert': 'equal'},
            {'cards': ['A', 'A'],  'expected': 'AA',  'assert': 'equal'},
            {'cards': ['5', '5'],  'expected': '55',  'assert': 'equal'},
            {'cards': ['7', 'A'],  'expected': 'A7',  'assert': 'equal'},
            {'cards': ['J', '10'], 'expected': 'TT',  'assert': 'equal'},
            {'cards': ['J', 'J'],  'expected': 'TT',  'assert': 'equal'},
            {'cards': ['2', '3', '4'], 'expected': '9', 'assert': 'equal'},
            {'cards': ['K', 'Q', 'J'], 'expected': '30', 'assert': 'equal'},
            {'cards': ['5', '5', '5'], 'expected': '15', 'assert': 'equal'},
            {'cards': ['10', '5', '2', 'J'], 'expected': '15', 'assert': 'notEqual'},
            {'cards': ['2', '3', '4', '6', 'A'], 'expected': '19', 'assert': 'equal'},
            ]

        #build test hand
        for case in test_values:
            hand = Hand()
            for card_value in case['cards']:
                hand.cards.append(Card(card_value)) #Add cards to test_hand
            expected_value = case['expected']
            actual = hand.get_formatted_hand_total()

            if case['assert'] == 'equal':
                self.assertEqual(actual, expected_value, 
                             "formatted hand string not equal")

            elif case['assert'] == 'notEqual':
                self.assertNotEqual(actual, expected_value, 
                             "formatted hand string equal")


if __name__ == '__main__':
    unittest.main()