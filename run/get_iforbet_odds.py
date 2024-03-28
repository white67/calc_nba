# get current nba odds

import sys
import time
sys.path.append('')
from config.config import *
from config.cfg_bookmaker import *
from config.cfg_database import *
import math

import mysql.connector

###

# retrieve json file from API and save it to json file
def get_iforbet_odds(bookmaker):
    
    # make connection
    db, mycursor = db_connect()
    
    time.sleep(sleep_random(API_TIMEOUT))
    
    # now we need to look for specific day matches, so take input from config file
    date_str = EVENTS_DATE
    date = datetime.strptime(date_str, '%Y-%m-%d')
    start_date = date + timedelta(hours=15)
    end_date = start_date + timedelta(days=1)
    start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
    end_date_str = end_date.strftime('%Y-%m-%d %H:%M:%S')
    
    # get request
    response = requests.get(url_iforbet_upcoming, headers=api_headers_common)


    # check api status code
    if response.status_code == 200:
        print("Code: 200")
        
        # get all events ids and then parse to api one-by-one
        response = response.json()
        
        eventsId_of_upcoming_matches = []
        
        for match in response["data"]:
            
            # check sportId and tournamentId and ((timestamp) -> later) to retrieve only matches from specified day
            if match["category1Id"] == category1Id_iforbet and match["category2Id"] == category2Id_iforbet and match["category3Id"] == category3Id_iforbet:
                eventsId_of_upcoming_matches.append(match["eventId"])
        
        # having all events id, we can go and call some APIs
        counter = 1
        for event in eventsId_of_upcoming_matches:
            
            # sleeping before requests
            time.sleep(sleep_random(API_TIMEOUT))
            
            print(f"{counter}. Getting response for {event}...")
            response = requests.get(cfg_url_iforbet(event), headers=api_headers_common)
            
            if response.status_code == 200:
                print("\n\nCode: 200")
                
                # get all events ids and then parse to api one-by-one
                response = response.json()
                
                print(f"{response["data"]["eventStart"]}")
                # event_datetime = correct_date_timestamp(response["data"]["eventStart"])
                ev = response["data"]["eventStart"]/1000
                event_datetime = datetime.fromtimestamp(ev)
                
                # event_datetime = datetime.strptime(event_datetime, '%Y-%m-%d %H:%M:%S')
                # event_datetime += timedelta(hours=1)
                # event_datetime = event_datetime.strftime('%Y-%m-%d %H:%M:%S')
                
                print(f"event_datetime: {event_datetime}")
                
                matchName = response["data"]["eventName"]
                teams = []
                for team in response["data"]["participants"]:
                    teams.append(team["name"].split()[-1])
                    
                print(f"teams[0]: {teams[0]}")
                print(f"teams[1]: {teams[1]}\n\n")
                
                for bet in response["data"]["eventGames"]:
                    player_name = None
                    player_id = None
                    refers_single_player = None
                    refers_multiple_players = None
                    bet_full_info = None
                    bet_name = bet["gameName"]
                    
                    pattern = bet["gameTypePattern"]
                    if "{%player}" in pattern:
                        # print(f"{bet_name}")
                        bet_name_patterns = bet_name.split(" - ")[0]
                        if "," in bet_name_patterns:
                            bet_name_patterns = bet_name_patterns.split(", ")
                            player_name = f"{bet_name_patterns[1]} {bet_name_patterns[0]}"
                        else:
                            player_name = bet_name_patterns
                        
                        refers_single_player = True
                        refers_multiple_players = False
                        player_id = get_id(mycursor, PLAYERS_PLAYER_ID, PLAYERS, [PLAYERS_PLAYER_NAME, PLAYERS_TEAM], [player_name, teams[0]])
                        if player_id == None:
                            player_id = get_id(mycursor, PLAYERS_PLAYER_ID, PLAYERS, [PLAYERS_PLAYER_NAME, PLAYERS_TEAM], [player_name, teams[1]])
                            if player_id == None:
                                # there are no players with this name and any of the 2 teams (playing) in database PLAYERS
                                pass
                        
                        print(f"{player_id} | {player_name}") if player_id == None else ""
                    
                    for outcome in bet["outcomes"]:
                        
                        bet_outcome = outcome["outcomeName"]
                        bet_odds = outcome["outcomeOdds"]
                        active_status = True if outcome["status"] == 100 else False
                        match_id = get_id(mycursor, MATCHES_MATCH_ID, MATCHES, [MATCHES_TEAM1, MATCHES_TEAM2, MATCHES_MATCH_DATE], [teams[0], teams[1], event_datetime])
                        
                        # print("### Data to be added to BETS database:")
                        # print(
                        #     f"bet_name: {bet_name}\n" +
                        #     f"bet_outcome: {bet_outcome}\n" +
                        #     f"bet_odds: {bet_odds}\n" +
                        #     f"bet_full_info: {bet_full_info}\n" +
                        #     f"player_id: {player_id}\n" +
                        #     f"match_id: {match_id}\n" +
                        #     f"refers_single_player: {refers_single_player}\n" +
                        #     f"refers_multiple_players: {refers_multiple_players}\n" +
                        #     f"active_status: {active_status}\n" +
                        #     f"bookmaker: {bookmaker}"
                        # )

                        # save bet info in database
                        db_add(db, mycursor, BETS, [BETS_NAME, BETS_OUTCOME, BETS_ODDS, BETS_FULL_INFO, BETS_PLAYER_ID, BETS_MATCH_ID, BETS_REFERS_SINGLE, BETS_REFERS_MULTIPLE, BETS_ACTIVE_STATUS, BETS_BOOKMAKER], [bet_name, bet_outcome, bet_odds, bet_full_info, player_id, match_id, refers_single_player, refers_multiple_players, active_status, bookmaker])
                        
                        # get bet_id to add connections
                        bet_id = get_id(mycursor, BETS_BET_ID, BETS, [BETS_NAME, BETS_OUTCOME, BETS_ODDS, BETS_BOOKMAKER], [bet_name, bet_outcome, bet_odds, bookmaker])
                        
                        if player_id != None:
                            # add bet connection to database
                            db_add(db, mycursor, BETS_ASSIGNED, [BETS_ASSIGNED_BET_ID, BETS_ASSIGNED_PLAYER_ID], [bet_id, player_id])
            counter += 1
                        
                    
    elif response.status_code == 404:
        print(f"Code: 404")
    else:
        print("Request failed with status code:", response.status_code)
        
    # Close the cursor and connection
    mycursor.close()
    db.close()

if __name__ == "__main__":
    get_iforbet_odds(BOOKMAKER_IFORBET)