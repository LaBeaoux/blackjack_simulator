from blackkjack_globals import *


class Hand():
    def __init__(self, hand_wager=0):
        """
        cards = list of Card() objects for each card in the hand
        sum = initial total of all cards
        blackjack = If 21 was hit on the nose
        bust = If sum is greater than 21
        """
        self.cards = []
        self.sum = 0
        self.blackjack = False
        self.bust = False
        self.surrender = False
        self.wager = hand_wager

    def get_formatted_hand_total(self):
        """
        This method returns the total of a hand in string form as needed by rulesets.
        If an Ace is in the hand the ace will lead the string, e.g. 'A8', 'A10', 'A19'
        Otherwise the string version of the integer will be returned, e.g. '9', '17', '21', '24'
        If an Ace is present, and the hand is bust the Ace will be counted numerically and returned 
          as an int str, e.g. '23'. This condition will be handled from the calling function
        """
        values = []
        formatted_hand_total = ""

        for card in self.cards:
            values.append(card.value)

        if len(self.cards) == 2:
            if 'A' in values:
                formatted_hand_total = self.__evaluate_ace_in_two_cards(values)
            else:
                formatted_hand_total = self.__evaluate_two_cards(values)

        elif len(self.cards) > 2:
            #If more than 2 cards are out, use the numeric totals of all card other than the ace
            if 'A' in values:
                formatted_hand_total = self.__evaluate_ace_in_large_hand(values)
            else:
                #If no Ace is present, sum up values of all cards
                formatted_hand_total = self.__evaluate_large_hand(values)

        #formatted hand total will only ever have one leading Ace if multiples are present (e.g. 'A4' or 'A18')
        return formatted_hand_total

    def __evaluate_ace_in_two_cards(self, values):
        if values[0] == values[1]:
            #If both are aces return the following
            formatted_hand_total = 'AA'
        else:
            #Get the 'A' first in the string
            if values[0] == 'A':
                formatted_hand_total = values[0] + values[1]
            else:
                formatted_hand_total = values[1] + values[0]
            
            #Convert face cards to 10
            if formatted_hand_total[1] in ['K', 'Q', 'J']:
                formatted_hand_total = 'A10'

        return formatted_hand_total

    def __evaluate_two_cards(self, values):
        if values[0] == values[1]:
            if CARD_VALUES[values[1]] == 10:
                #If cards are the same value and worth 10, need to return 'TT'
                formatted_hand_total = 'TT'
            else:
                #Check for 'same' card for 'special' rules. Return '22', '66', etc. format
                formatted_hand_total = values[0] + values[1]
        else:
            #Add values if neither is Ace
            formatted_hand_total = str(CARD_VALUES[self.cards[0].value] + CARD_VALUES[self.cards[1].value])
        return formatted_hand_total

    def __evaluate_ace_in_large_hand(self, values):
        formatted_hand_total = ""
        a_index = None

        for index, value in enumerate(values):
            if value == 'A':
                if a_index != None:
                    #If multiple Aces are in deck and 1st Ace has been found, since both can't be high all others MUST be 1's
                    values[index] = '1'
                else:
                    a_index = index

        formatted_hand_total += values.pop(a_index) #Get the Ace 'A' first
        
        #Sum integer values of remaining cards.
        remaining_cards_total = 0
        for value in values:
            remaining_cards_total += CARD_VALUES[value]

        if remaining_cards_total > 10:
            #If the remaining cards are above a value of 10, then Ace-High (11) is no longer viable.
            #Turn the Ace to a 1 and treat it all as an int str
            formatted_hand_total = str(remaining_cards_total + 1)
        else:
            formatted_hand_total += str(remaining_cards_total) #Keep the leading 'A'

        #Check for non-Ace value being over 10, if so return A11
        temp_total = formatted_hand_total[1::]
        if int(temp_total) >= 11:
            formatted_hand_total = 'A11'

        return formatted_hand_total

    def __evaluate_large_hand(self, values):
        total = 0
        for value in values:
            total += CARD_VALUES[value]
        formatted_hand_total = str(total)
        return formatted_hand_total

    def blackjack_or_bust(self):
        """
        This method sets blackjack or bust parameters for the hand.
        """
        values = [card.value for card in self.cards]
        if 'A' in values:
            #Check for blackjack
            sum = 0
            multiple_aces = False
            for index in range(len(values)):
                if values[index] != 'A':
                    sum += int(CARD_VALUES[values[index]])
                elif values[index] == 'A':
                    if multiple_aces:
                        #Make every Ace other than the first have a '1' value
                        values[index] = '1'

            if sum == 10:
                #Accounting for Ace==11
                self.blackjack = True
            elif sum == 20:
                #Accounting for Ace==1
                self.blackjack = True
            elif sum > 21:
                self.bust = True
        else:
            sum = 0 
            for value in values:
                sum += int(CARD_VALUES[value])
            if sum == 21:
                self.blackjack = True
            elif sum > 21:
                self.bust = True

    def evaluate_dealer_hand(self):
        sum = 0
        for card in self.cards:
            sum += card.get_value


