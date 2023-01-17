from blackkjack_globals import *
from rulesets import ruleset_template


class Standard_Dealer_Hits_Soft_17_Ruleset(ruleset_template.Ruleset_Template):
    def __init__(self):
        self.ruleset_table_name = "standard_dealer_hits_soft_17"
        super().__init__(self.ruleset_table_name)
        
    def get_action_from_ruleset(self, hand_total, dealer_upcard):
        """
        Generic get-aciton method from which to build more complicated decisions from
        """
        #TODO: Consider keeping db connection open entire time?
        conn = self.create_connection()
        action = self.retreive_ruleset_action(conn, hand_total, dealer_upcard)
        self.close_database(conn)
        return action
        