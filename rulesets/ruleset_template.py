import sqlite3
from blackkjack_globals import *

class Ruleset_Template():
    def __init__(self, ruleset_table_name):
        self.db = "/Users/aaronlabomascus/Projects/blackjack/rulesets/blackjack_player_rules.db"
        self.ruleset_table_name = ruleset_table_name

    def create_connection(self):
        """
        Create connection to sqlite3 database file
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db)
        except Exception as e:
            print(e)

        return conn

    def close_database(self, conn):
        conn.close()

    def retreive_ruleset_action(self, conn, hand_total, dealer_upcard):
        """
        Input: A valid sqlite3 connection object to a database
        Objective: Return the action to take in the specified ruleset according to 
                the hand_total and dealer_updcard
        """
        cur = conn.cursor()
        cur.execute(f"""SELECT "{dealer_upcard}" FROM {self.ruleset_table_name} WHERE hand_total='{hand_total}' """)
        
        results = cur.fetchall()
        assert len(results[0]) == 1
        action = results[0][0]
        return action