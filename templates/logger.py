class Logger():
    def __init__(self):
        pass

    def log_hands(self, player_num, player_hand, dealer_hand, num_hands_played):
        ph = player_hand.get_formatted_hand_total()
        player_cards = [card.value for card in player_hand.cards]
        dh = dealer_hand.get_formatted_hand_total()
        dealer_cards = [card.value for card in dealer_hand.cards]
        print(f"Number of Deals: {num_hands_played}")
        print(f"Player {player_num} Hand: {player_cards} = {ph}, Dealer Hand: {dealer_cards} = {dh}")

    def log_result(self, result):
        print(f"Result: {result}")

    def log_player_chips(self, player, player_num):
        print(f"Player {player_num} chips: ${player.chips}")