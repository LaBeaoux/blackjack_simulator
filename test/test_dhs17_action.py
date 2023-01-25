import unittest
import sys

from blackkjack_globals import *
from rulesets.dealer_rulesets import get_dhs17_ruleset_action
from rulesets import standard_dealer_hits_soft_17_ruleset as std_dhs17
from templates.hand import Hand
from templates.card import Card
from templates.player import Player

sys.path.append("/Users/aaronlabomascus/Projects/blackjack") #Necessary... Not sure why yet

"""
To run unittest class:
from commandline of project root, e.g. /Users/<user>/Projects/blackjack
 - run `python -m unittest test.test_dhs17_action`
Or to find and run all available unit tests
 - run `python -m unittest discover
There are also alternatives to specify specific test functions only
"""

class TestDHS17RulesetAction(unittest.TestCase):

    def test_get_dhs17_ruleset_action(self):
        DEALER = Player(get_dhs17_ruleset_action)

        test_values = [
            {'cards': ['10', '6'],  'expected': HIT},
            {'cards': ['10', '7'],  'expected': STAY},
            {'cards': ['10', '8'],  'expected': STAY},
            {'cards': ['2', '3'],  'expected': HIT},
            {'cards': ['J', 'A'],  'expected': STAY},
            {'cards': ['A', 'A'],  'expected': HIT},
            {'cards': ['5', '5'],  'expected': HIT},
            {'cards': ['7', 'A'],  'expected': STAY},
            {'cards': ['J', '10'], 'expected': STAY},
            {'cards': ['J', 'J'],  'expected': STAY},
            {'cards': ['2', '3', '4'], 'expected': HIT},
            {'cards': ['K', 'Q', 'J'], 'expected': STAY},
            {'cards': ['5', '5', '5'], 'expected': HIT},
            {'cards': ['10', '5', '2', 'J'], 'expected': STAY},
            {'cards': ['2', '3', '4', '6', 'A'], 'expected': HIT},
            ]
        
        #Create Hand objects to from test values to pass to ruleset action
        for case in test_values:
            hand = Hand()

            print(f"Cards: {case['cards']}")
            for card_value in case['cards']:
                hand.cards.append(Card(card_value)) #Add cards to test_hand

            expected_value = case['expected']
            DEALER.hands = [hand]
            actual = DEALER.get_dealer_action()

            print(f"Expected: {expected_value}, Actual: {actual}")
            self.assertEqual(actual, expected_value)

if __name__ == '__main__':
    unittest.main(verbosity=9)