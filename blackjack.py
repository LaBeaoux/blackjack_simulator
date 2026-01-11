import random
import sqlite3
import sys

from blackkjack_globals import *
from templates import Card
from templates import Hand
from templates import Player
from templates import Logger

from rulesets import dealer_rulesets
from rulesets import standard_dealer_hits_soft_17_ruleset as std_dhs17
from metrics import Metrics


DEALER = Player(dealer_rulesets.get_dhs17_ruleset_action)
PLAYERS = []
SHOE = []
MINIMUM_BET = 50
logger = Logger()
METRICS = None
ROTATION_DECKS = 7
MAX_HANDS = 10000
INITIAL_SHOE_SIZE = 0
RESHUFFLE_FRACTION = 0.25
INTERACTIVE = False
HUMAN_PLAYER_INDEX = 0
STARTING_CHIPS = 100000

def create_shoe(decks:int=7):
    shoe = []
    for i in range(decks):
        for j in range(len(SUITS)):
            for value in VALUES:
                card = Card(value)
                shoe.append(card)
    return shoe

def PLAYERS_AT_TABLE(player_count):
    global PLAYERS
    PLAYERS.clear()
    for _ in range(player_count):
        PLAYERS.append(Player(ruleset=std_dhs17.Standard_Dealer_Hits_Soft_17_Ruleset(),
                              chips=STARTING_CHIPS,
                              min_wager=MINIMUM_BET))

def enough_cards_in_shoe():
    # Deprecated for rotation mode: keep returning True since we reshuffle when needed.
    return True

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
    card = draw_card()
    hand.cards.append(card)


def draw_card():
    """Pop a card from the shoe or raise RuntimeError if the shoe is empty."""
    global SHOE
    if not SHOE:
        raise RuntimeError("Shoe depleted - ending game")
    return SHOE.pop(0)

def player_action_HIT(player,hand):
    add_card_to_hand(hand)
    hand.blackjack_or_bust()

def player_action_DOUBLE_DOWN(player, hand):
    player.chips -= hand.wager
    hand.wager *= 2
    player_action_HIT(player, hand)

def player_action_SPLIT(player, hand, dealer_upcard, player_index=None):
    # Split the specified hand into two hands, preserving other hands at the table
    try:
        index = player.hands.index(hand)
    except ValueError:
        return

    if len(hand.cards) < 2:
        return

    wager = hand.wager
    # Take the two original cards
    card1 = hand.cards[0]
    card2 = hand.cards[1]

    new_hand1 = Hand(wager)
    new_hand2 = Hand(wager)

    new_hand1.cards.append(card1)
    new_hand1.cards.append(draw_card())

    new_hand2.cards.append(card2)
    new_hand2.cards.append(draw_card())

    # Replace the original hand with the two new hands in-place
    player.hands[index:index+1] = [new_hand1, new_hand2]

    # Evaluate the newly created hands
    evaluate_player_actions(player, new_hand1, dealer_upcard, player_index)
    evaluate_player_actions(player, new_hand2, dealer_upcard, player_index)

def evaluate_player_actions(player, hand, dealer_upcard, player_index=None):
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
        
        if INTERACTIVE and player_index == HUMAN_PLAYER_INDEX:
            action = prompt_for_player_action(player, hand, dealer_upcard)
        else:
            action = player.action(hand_total, dealer_upcard)

        if action == HIT:
            player_action_HIT(player, hand)

        elif action == STAY:
            break

        elif action == DOUBLE_DOWN:
            player_action_DOUBLE_DOWN(player, hand)
            break

        elif action == SPLIT:
            player_action_SPLIT(player, hand, dealer_upcard, player_index)
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
    for player_index, player in enumerate(PLAYERS):
        for hand_index in range(len(player.hands)):
            hand = player.hands[hand_index]
            dealer_upcard = DEALER.hands[0].cards[0].value
            # logger.log_hands(0, hand, DEALER.hands[0],0)

            evaluate_player_actions(player, hand, dealer_upcard, player_index)

    #After all players are done, DEALER plays hand        
    evaluate_dealer_actions()

def compare_formatted_hand_values(dealer_hand, player_hand):
    """
    returns "DEALER", "PLAYER", or "DRAW" for tie
    """
    #The assumption is that all player and dealer blackjack/busts are evaluated before this function is run
    
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
            # Determine outcome and update chips
            win = False
            if hand.blackjack:
                # Return initial wager + 3/2 wager to player's chips
                player.chips += ((5/2) * hand.wager)
                logger.log_result("Player Blackjack")
                win = True
            elif hand.bust or dealer_hand.blackjack:
                # chips in hand.wager will disappear when object is deconstructed at end of hand
                logger.log_result("Player Loses")
                win = False
            elif dealer_hand.bust:
                # Payout wager as a win (return wager + winnings)
                player.chips += (2 * hand.wager)
                logger.log_result("Dealer Bust, Player wins")
                win = True
            else:
                outcome = compare_formatted_hand_values(dealer_hand, hand)
                if outcome == "PLAYER":
                    logger.log_result("Player wins")
                    player.chips += (2 * hand.wager)
                    win = True
                elif outcome == "DEALER":
                    # chips in hand.wager will disappear when hand object is deconstructed at end of deal
                    logger.log_result("Dealer wins")
                    win = False
                elif outcome == "DRAW":
                    # wager returns to players pot
                    logger.log_result("Draw")
                    player.chips += hand.wager
                    win = False

            # Record metrics if enabled
            if METRICS is not None:
                METRICS.record_hand(player_num, player.chips, win)
            
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
    SHOE = create_shoe(decks=ROTATION_DECKS)
    global INITIAL_SHOE_SIZE
    INITIAL_SHOE_SIZE = len(SHOE)
    r = random.SystemRandom()
    r.shuffle(SHOE)


def check_and_reshuffle_if_needed():
    """If the shoe size falls below a practical minimum, reshuffle the full rotation."""
    # Use a conservative threshold: reshuffle when shoe falls below RESHUFFLE_FRACTION
    # of the initial shoe size, but at least one full deck worth of cards.
    min_by_fraction = int(INITIAL_SHOE_SIZE * RESHUFFLE_FRACTION) if INITIAL_SHOE_SIZE > 0 else 0
    min_by_deck = len(SUITS) * len(VALUES)
    min_cards = max(min_by_fraction, min_by_deck)

    if len(SHOE) <= min_cards:
        print(f"Shoe reached minimum ({len(SHOE)} <= {min_cards}) — reshuffling {ROTATION_DECKS} decks")
        prepare_the_shoe()


def prompt_for_player_action(player, hand, dealer_upcard):
    """Interactively prompt the human player for an action.

    Returns the mapped global action integer (HIT/STAY/etc).
    Raises ValueError for invalid choices.
    """
    valid_chars = {'H', 'S', 'D', 'P', 'R'}
    while True:
        # Display info
        player_cards = [c.value for c in hand.cards]
        print(f"Your hand: {player_cards} = {hand.get_formatted_hand_total()}")
        print(f"Dealer upcard: {dealer_upcard}")
        choice = input("Choose action [H=Hit, S=Stay, D=Double, P=Split, R=Surrender]: ").strip().upper()
        if choice not in valid_chars:
            print("Invalid action. Use one of H,S,D,P,R.")
            continue

        # Validate action feasibility
        if choice == 'D':
            if player.chips < hand.wager:
                print("Not enough chips to double down.")
                continue
        if choice == 'P':
            # Can only split when exactly two cards of same value and enough chips
            if len(hand.cards) != 2 or hand.cards[0].value != hand.cards[1].value:
                print("Cannot split: hand is not a pair.")
                continue
            if player.chips < hand.wager:
                print("Not enough chips to split.")
                continue

        # Map to globals
        action = map_actions_to_globals(choice)
        return action


def main():
    prepare_the_shoe()

    PLAYERS_AT_TABLE(1)
    global METRICS
    METRICS = Metrics(len(PLAYERS))
    hands_count = 0

    try:
        while True:
            # Stop if we've reached the requested number of hands
            if MAX_HANDS is not None and hands_count >= MAX_HANDS:
                print(f"Reached max_hands={MAX_HANDS}")
                break

            # Ensure the shoe has enough cards; reshuffle rotation if low
            check_and_reshuffle_if_needed()

            hands_count += 1
            broke = make_bets()
            if broke:
                print("Player broke while betting")
                break

            deal_first_two_cards()
            play_out_hand()
            compare_player_hands_to_house_hand(hands_count)
            clear_cards_from_table()
            print('\n\n')

            # Stop if any player cannot meet their minimum wager
            for p_idx, p in enumerate(PLAYERS):
                if p.chips < p.wager or p.chips <= 0:
                    print(f"Player {p_idx} out of chips (chips={p.chips}) - ending session")
                    raise RuntimeError("Player out of money - ending game")
    except RuntimeError as e:
        print(e)
    print("GAME OVER! Hands played:", hands_count)

    # Save metrics artifacts
    if METRICS is not None:
        METRICS.save_csv("metrics_chips.csv")
        METRICS.save_summary("metrics_summary.csv")
        METRICS.print_summary()
        try:
            METRICS.plot_chips("metrics_chips.png", show=False)
            print("Saved plot to metrics_chips.png")
        except Exception as e:
            print(f"Failed to save plot: {e}")
    #TODO: Test out general game functionality
    #TODO: Build out metric tracking, results storage, and analytics analysis

if __name__ == "__main__":
    main()