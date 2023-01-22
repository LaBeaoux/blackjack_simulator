import random
import sqlite3

from blackkjack_globals import *
from templates import Card
from templates import Hand
from templates import Player
from templates import Logger

from rulesets import dealer_rulesets
from rulesets import standard_dealer_hits_soft_17_ruleset as std_dhs17


DEALER = Player(dealer_rulesets.get_dhs17_ruleset_action)
PLAYERS = []
SHOE = []
logger = Logger()

def create_shoe(decks:int=1):
    shoe = []
    for i in range(decks):
        for j in range(len(SUITS)):
            for value in VALUES:
                card = Card(value)
                shoe.append(card)
    return shoe

def PLAYERS_AT_TABLE(player_count):
    for player in range(player_count):
        PLAYERS.append(Player(ruleset=std_dhs17.Standard_Dealer_Hits_Soft_17_Ruleset(),
                              chips=1000,
                              min_wager=15))

def enough_cards_in_shoe():
    if len(SHOE) > (len(PLAYERS) * 4):
        return 1
    else:
        print("Cards running Low! Game Over!")
        return 0

def deal_first_two_cards():
    #Deal 2 cards per player
    
    for player in PLAYERS:
        player.hands.append(Hand(player.wager))
        for turn in range(2):
            for hand in player.hands:
                add_card_to_hand(hand)

    DEALER.hands.append(Hand())
    add_card_to_hand(DEALER.hands[0])
    add_card_to_hand(DEALER.hands[0])

    #Have the players tally up their first two cards to check for game ending conditions
    for player in PLAYERS:
        for hand in player.hands:
            hand.blackjack_or_bust()

def add_card_to_hand(hand):
    card = SHOE.pop(0)
    hand.cards.append(card)

def player_action_HIT(player,hand):
    add_card_to_hand(hand)
    hand.blackjack_or_bust()

def player_action_DOUBLE_DOWN(player, hand):
    player.chips -= hand.wager
    hand.wager *= 2
    player_action_HIT(player, hand)

def player_action_SPLIT(player, hand, dealer_upcard):
    card = hand.cards[0] #Only need to specify one since they are the same
    wager = hand.wager
    player.hands = [Hand(wager), Hand(wager)]
    for hand in player.hands:
        hand.cards.append(card)
        hand.cards.append(SHOE.pop(0))
        #Since original hand wasn't identified in play_out_hand() need to call this recursively to execute on the "new" hand(s)
        evaluate_player_actions(player, hand, dealer_upcard)

def evaluate_player_actions(player, hand, dealer_upcard):
    """
     This method outlines the phase where the player takes actions up until they have no further moves availble
    """
    while not (hand.blackjack or hand.bust or hand.surrender):
        #Continue operating on player actions until a STAY, BUST, OR BLACKJACK is had (or if DOUBLE_DOWN is performed)

        hand_total = hand.get_formatted_hand_total()

        if ('A' not in hand_total and 'T' not in hand_total):
            if (int(hand_total) > 21):
                hand.bust = True
                continue
        
        action = player.action(hand_total, dealer_upcard)

        if action == HIT:
            player_action_HIT(player, hand)

        elif action == STAY:
            break

        elif action == DOUBLE_DOWN:
            player_action_DOUBLE_DOWN(player, hand)
            break

        elif action == SPLIT:
            player_action_SPLIT(player, hand, dealer_upcard)
            break

        elif action == SURRENDER:
            hand.surrender = True
            player.chips += (0.5 * hand.wager)

        elif action == DOUBLE_DOWN_ELSE_SURRENDER:
            print("TODO: DOUBLE_DOWN_ELSE_SURRENDER implementation")

        else:
            print(f"ACTION {action} UNKNOWN!")

def evaluate_dealer_actions():
    while not (DEALER.hands[0].blackjack or DEALER.hands[0].bust):
        action = DEALER.get_dealer_action()
        if action == HIT:
            add_card_to_hand(DEALER.hands[0])
            DEALER.hands[0].blackjack_or_bust()
        elif action == STAY:
            break

def play_out_hand():
    #Play out all Players actions
    for player in PLAYERS:
        for hand_index in range(len(player.hands)):
            hand = player.hands[hand_index]
            dealer_upcard = DEALER.hands[0].cards[0].value
            logger.log_hands(0, hand, DEALER.hands[0],0)

            evaluate_player_actions(player, hand, dealer_upcard)

    #After all players are done, DEALER plays hand        
    evaluate_dealer_actions()

def compare_formatted_hand_values(dealer_hand, player_hand):
    """
    returns "DEALER", "PLAYER", or "DRAW" for tie
    """
    #The assumption is that all player an dealer blackjack/busts are evaluated before this function is run
    
    dealer_total, player_total = get_integer_totals(dealer_hand, player_hand)
        
    if dealer_total > player_total:
        return "DEALER"
    elif player_total > dealer_total:
        return "PLAYER"
    elif player_total == dealer_total:
        return "DRAW"

def compare_player_hands_to_house_hand(round):
    """
    Look at each players hand
    If Blackjack, pay ratio
    If Bust, do nothing (cleaning hands will void their wagers)
    Else compare counts for WIN, LOSS, or PUSH
    """
    dealer_hand = DEALER.hands[0]
    for player_num, player in enumerate(PLAYERS):
        for hand in player.hands:

            logger.log_hands(player_num, hand, dealer_hand, round)

            dealer_hand = DEALER.hands[0]
            
            if hand.blackjack:
                #Return initial wager + 3/2 wager to player's chips
                player.chips += ((5/2) * hand.wager)
                logger.log_result("Player Blackjack")
                continue

            elif hand.bust or dealer_hand.blackjack:
                #chips in hand.wager will disappear when object is deconstructed at end of hand
                logger.log_result("Player Loses")
                continue

            elif dealer_hand.bust:
                #Payout wager
                player.chips += hand.wager
                logger.log_result("Dealer Bust, all Players Win")
                continue

            outcome = compare_formatted_hand_values(dealer_hand, hand)

            if outcome == "PLAYER":
                logger.log_result("Player wins")
                player.chips += (2 * hand.wager)

            elif outcome == "DEALER":
                #chips in hand.wager will disappear when hand object is deconstructed at end of deal
                logger.log_result("Dealer wins")

            elif outcome == "DRAW":
                #wager returns to players pot
                logger.log_result("Draw")
                player.chips += hand.wager
            
def make_bets():
    for player in PLAYERS:

        if player.chips < player.wager:
            print("PLAYER out of chips!!! Stop game!")
            return True

        #TODO: Add ability to change initial wager if desired before cards dealt
        player.chips -= player.wager
    return False

def clear_cards_from_table():
    for player_num, player in enumerate(PLAYERS):
        player.hands = []
        logger.log_player_chips(player, player_num)
    DEALER.hands = []

def prepare_the_shoe():
    global SHOE
    SHOE = create_shoe(decks=1)
    r = random.SystemRandom()
    r.shuffle(SHOE)

def main():
    prepare_the_shoe()

    PLAYERS_AT_TABLE(1)
    hands_count = 0

    while enough_cards_in_shoe():
        hands_count += 1
        broke = make_bets()
        if broke:
            break
        deal_first_two_cards()
        play_out_hand()
        compare_player_hands_to_house_hand(hands_count)
        clear_cards_from_table()

    print("GAME OVER!")
    #TODO: Test out general game functionality
    #TODO: Build out metric tracking, results storage, and analytics analysis

if __name__ == "__main__":
    main()