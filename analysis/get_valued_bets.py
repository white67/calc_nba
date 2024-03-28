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

all_bet_names = {}

# Execute the SQL query
datetime_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
mycursor.execute(f'SELECT match_id FROM matches WHERE match_date > "{datetime_now}"')

# Fetch all the results
matches = mycursor.fetchall()

# Loop through the results
counter_over = 0
counter_under = 0
count_other = 0


for match in matches:
    match_id = match[0]  # Assuming match_id is the first column
    # Do something with match_id, for example:
    mycursor.execute(f'select player_id, bet_name, outcome, odds_value from bets where bookmaker = "superbet" and match_id = {match_id} and refers_single_player = 1;')
    bets = mycursor.fetchall()
    
    for single_bet in bets:
        if single_bet[0] != None:
            znak = ""
            
            player_id = single_bet[0]
            mycursor.execute(f'select player_name from players where player_id = {player_id}')
            player_name = mycursor.fetchall()
            stats_to_focus = convert_bet_name(single_bet[1])
            outcome = single_bet[2]
            # print(f"bet: {player_name}", single_bet)
            
            if stats_to_focus != None:
                # count bet_names with " - " inside
                if "powyżej" in outcome.lower() or "poniżej" in outcome.lower():
                    value = outcome.split(" - ")[1].split(" ")[1]
                    
                    znak = ">" if "powyżej" in outcome.lower() else "<"
                    
                    if len(stats_to_focus) == 1:
                        stats_string = stats_to_focus[0]
                        stats_addition = stats_string
                    else:
                        stats_string = ', '.join(stats_to_focus)
                        stats_addition = "+".join(stats_to_focus)
                    
                    # count all previous number of matches for this player
                    mycursor.execute(f"select count(stat_id) from stats LEFT JOIN matches ON stats.match_id = matches.match_id where player_id = {player_id} order by matches.match_date desc;")
                    last_all = mycursor.fetchall()
                    number_of_matches = last_all[0][0]
                    
                    # print(f"number_of_matches: {number_of_matches}")
                    
                    # last all-time
                    mycursor.execute(f"select count({stats_to_focus[0]}) from (select {stats_string} from stats LEFT JOIN matches ON stats.match_id = matches.match_id where player_id = {player_id} order by matches.match_date desc) as xd where {stats_addition} {znak} {value};")
                    last_all = mycursor.fetchall()
                    
                    
                    last_value = last_all[0][0]
                    last_all_perc = last_value/number_of_matches
                    
                    # last 5
                    limit = 5
                    mycursor.execute(f"select count({stats_to_focus[0]}) from (select {stats_string} from stats LEFT JOIN matches ON stats.match_id = matches.match_id where player_id = {player_id} order by matches.match_date desc limit {limit}) as xd where {stats_addition} {znak} {value};")
                    last_5 = mycursor.fetchall()
                    last_value = last_5[0][0]
                    last_5_perc = last_value/5
                    
                    # last 10
                    limit = 10
                    mycursor.execute(f"select count({stats_to_focus[0]}) from (select {stats_string} from stats LEFT JOIN matches ON stats.match_id = matches.match_id where player_id = {player_id} order by matches.match_date desc limit {limit}) as xd where {stats_addition} {znak} {value};")
                    last_10 = mycursor.fetchall()
                    last_value = last_10[0][0]
                    last_10_perc = last_value/10
                    
                    
                    if last_5_perc > 0.79 and last_10_perc > 0.79 and last_all_perc > 0.79:
                        print(f"{single_bet[1]}: {single_bet[2]} | Odds: {single_bet[3]} | Last 5: {last_5_perc} | Last 10: {last_10_perc} | Last all: {last_all_perc}")
                        
        else:
            # print(f"{single_bet} something wrong with player_id")
            pass

print("\n\n\n")
print(f"counter_over: {counter_over}")
print(f"counter_under: {counter_under}")
print(f"count_other: {count_other}")

# Close the cursor and connection
mycursor.close()