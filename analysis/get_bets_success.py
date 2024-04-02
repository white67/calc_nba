import sys
import time
sys.path.append('')
from config.config import *
from config.cfg_bookmaker import *
from config.cfg_database import *
from config.cfg_superbet import *
import math

import mysql.connector

# Connect to the database
db, mycursor = db_connect()

# superbet version
def superbet_success():
    
    mycursor.execute(f'SELECT bet_id, bet_name, player_id, match_id, outcome, success FROM bets WHERE refers_single_player = 1 and player_id is not null and bookmaker = "superbet" and success is null')
    bets = mycursor.fetchall()
    
    for bet in bets:
        bet_success = bet[5]
        if bet_success == None:
            print("None")
            
            bet_id = bet[0]
            bet_name = bet[1]
            player_id = bet[2]
            match_id = bet[3]
            outcome = bet[4]
            if " - " in outcome:
                outcome = outcome.split(" - ")
                
                if "Tak" not in outcome and "Nie" not in outcome:
                    # print(bet)
                    # print(outcome)
                    outcome_value = float(outcome[1].split(" ")[-1])
                    outcome_under_over = outcome[1].split(" ")[0]
                    stats_to_focus = convert_bet_name(bet_name)
                    
                    if stats_to_focus != None:
                        counter = 0
                        x = 0
                        for stat in stats_to_focus:
                            mycursor.execute(f'SELECT {stat} FROM stats WHERE player_id = "{player_id}" and match_id = "{match_id}"')
                            number = mycursor.fetchall()
                            if len(number) > 0:
                                number = number[0][0]
                                counter += int(number)
                                x+=1
                        if x > 0:
                            if outcome_under_over.lower() == "poniżej":
                                if counter < outcome_value:
                                    db_update(db, mycursor, BETS, [BETS_SUCCESS], [1], [BETS_BET_ID], [bet_id])
                                else:
                                    db_update(db, mycursor, BETS, [BETS_SUCCESS], [0], [BETS_BET_ID], [bet_id])
                            elif outcome_under_over.lower() == "powyżej":
                                if counter > outcome_value:
                                    db_update(db, mycursor, BETS, [BETS_SUCCESS], [1], [BETS_BET_ID], [bet_id])
                                else:
                                    db_update(db, mycursor, BETS, [BETS_SUCCESS], [0], [BETS_BET_ID], [bet_id])
        else:
            print("Already succeed")
            

superbet_success()

# Close the cursor and connection
mycursor.close()