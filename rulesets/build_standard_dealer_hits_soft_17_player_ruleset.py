import sqlite3 as sql

con = sql.connect("blackjack_player_rules.db")
cur = con.cursor()
"""
https://www.blackjackreview.com/wp/encyclopedia/multiple-deck/
 - Multi-deck basic strategy with No double-after-split (No DAS) pair table
 - Since MDBS table didn't show 5-8 I took the instructions from another table
Legend:
 H  - Hit
 D  - Double down
 S  - Stay
 R  - Surrender if possible, else Hit
 P  - Split
"""
#remove if it already exists
# cur.execute("DROP TABLE standard_dealer_hits_soft_17")
cur.execute("CREATE TABLE IF NOT EXISTS standard_dealer_hits_soft_17('hand_total', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'A')")

data = [
        ('5',   'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'),
        ('6',   'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'),
        ('7',   'H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'),
        ('8',   'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'),
        ('9',   'H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'),
        ('10',  'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'),
        ('11',  'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H'),
        ('12',  'H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'),
        ('13',  'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'),
        ('14',  'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'),
        ('15',  'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'R', 'H'),
        ('16',  'S', 'S', 'S', 'S', 'S', 'H', 'H', 'R', 'R', 'R'),
        ('17',  'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'),
        ('18',  'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'),
        ('19',  'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'),
        ('20',  'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'),
        ('21',  'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'),
        ('A2',  'H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'),
        ('A3',  'H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'),
        ('A4',  'H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'),
        ('A5',  'H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'),
        ('A6',  'H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'),
        ('A7',  'S', 'D' ,'D' ,'D' ,'D' ,'S', 'S', 'H', 'H', 'H'),
        ('A8',  'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'),
        ('A9',  'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'),
        ('A10', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'),
        ('A11', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'),

        ('AA',  'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'),
        ('22',  'P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'),
        ('33',  'P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'),
        ('44',  'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'),
        ('55',  'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'),
        ('66',  'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H', 'H'),
        ('77',  'P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'),
        ('88',  'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'),
        ('99',  'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'),
        ('TT',  'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P')
        ]

cur.executemany("INSERT INTO standard_dealer_hits_soft_17 VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
con.commit()

#Verify creation contents
cur.execute('SELECT * FROM standard_dealer_hits_soft_17')
for row in cur.fetchall():
    print(row)

con.close()