# get current nba odds

import sys
import time
sys.path.append('')
from config.config import *
from config.cfg_bookmaker import *
from config.cfg_database import *
from config.cfg_superbet import *
import math

import mysql.connector

###

# retrieve json file from API and save it to json file
def get_superbet_odds(bookmaker):
    
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
    response = requests.get(cfg_url_superbet_upcoming(start_date_str, end_date_str), headers=api_headers_common)

    # check api status code
    if response.status_code == 200:
        print("Code: 200")
        
        # get all events ids and then parse to api one-by-one
        response = response.json()
        
        eventsId_of_upcoming_matches = []
        
        for match in response["data"]:
            # check sportId and tournamentId and ((timestamp) -> later) to retrieve only matches from specified day
            if match["sportId"] == sportId_superbet and match["tournamentId"] == tournamentId_superbet:
                eventsId_of_upcoming_matches.append(match["eventId"])
        
        # having all events id, we can go and call some APIs
        counter = 1
        for event in eventsId_of_upcoming_matches:
            
            # sleeping before requests
            time.sleep(sleep_random(API_TIMEOUT))
            
            print(f"{counter}. Getting response for {event}...")
            response = requests.get(cfg_url_superbet(event), headers=api_headers_common)
            
            if response.status_code == 200:
                print("Code: 200")
                
                # get all events ids and then parse to api one-by-one
                response = response.json()
                
                event_datetime = response["data"][0]["matchDate"]
                event_datetime = datetime.strptime(event_datetime, '%Y-%m-%d %H:%M:%S')
                event_datetime += timedelta(hours=2)
                event_datetime = event_datetime.strftime('%Y-%m-%d %H:%M:%S')
                
                # print(f"event_datetime: {event_datetime}")
                
                matchName = response["data"][0]["matchName"]
                teams = matchName.split("·")
                teams[0] = teams[0].split(" ")[-1]
                teams[1] = teams[1].split(" ")[-1]
                
                teams[0] = wrong_team_name(teams[0])
                teams[1] = wrong_team_name(teams[1])
                
                match_id = get_id(mycursor, MATCHES_MATCH_ID, MATCHES, [MATCHES_TEAM1, MATCHES_TEAM2, MATCHES_MATCH_DATE], [teams[0], teams[1], event_datetime])
                
                print(f"teams: {teams[0]} - {teams[1]}")
                print(f"match_id: {match_id}")
                
                # print(f"match_id: {match_id}")
                
                # check if bets from this match has already been scraped
                superbet_scraped = get_id(mycursor, MATCHES_SUPERBET_SCRAPED, MATCHES, [MATCHES_TEAM1, MATCHES_TEAM2, MATCHES_MATCH_DATE], [teams[0], teams[1], event_datetime])
                

                if response["data"][0]["odds"] is not None and superbet_scraped == None and match_id != None:
                    for bet in response["data"][0]["odds"]:
                        player_id = None
                        refers_single_player = None
                        refers_multiple_players = None
                        bet_name = bet["marketName"]
                        bet_outcome = bet["name"]
                        bet_full_info = bet["info"]
                        bet_odds = bet["price"]
                        
                        if 'specifiers' in bet:
                            refers_single_player = check_player_refers_superbet(bet["specifiers"], "single")
                            
                            if refers_single_player:
                                player_id = get_id(mycursor, PLAYERS_PLAYER_ID, PLAYERS, [PLAYERS_PLAYER_NAME, PLAYERS_TEAM], [bet["specifiers"]["player"], teams[0]])
                                if player_id == None:
                                    player_id = get_id(mycursor, PLAYERS_PLAYER_ID, PLAYERS, [PLAYERS_PLAYER_NAME, PLAYERS_TEAM], [bet["specifiers"]["player"], teams[1]])
                                    if player_id == None:
                                        player_id = get_id(mycursor, PLAYERS_PLAYER_ID, PLAYERS, [PLAYERS_PLAYER_NAME], [bet["specifiers"]["player"]])
                                        if player_id == None:
                                            # there are no players with this name and any of the 2 teams (playing) in database PLAYERS
                                            pass
                                    
                            refers_multiple_players = check_player_refers_superbet(bet["specifiers"], "multiple")    
                        else:
                            refers_single_player = False
                            refers_multiple_players = False
                            player_id = None
                        
                        active_status = True if bet["status"] == "active" else False
                        
                        # print(f"event_datetime: {event_datetime}")
                        
                        # save bet info in database
                        db_add(db, mycursor, BETS, [BETS_NAME, BETS_OUTCOME, BETS_ODDS, BETS_FULL_INFO, BETS_PLAYER_ID, BETS_MATCH_ID, BETS_REFERS_SINGLE, BETS_REFERS_MULTIPLE, BETS_ACTIVE_STATUS, BETS_BOOKMAKER], [bet_name, bet_outcome, bet_odds, bet_full_info, player_id, match_id, refers_single_player, refers_multiple_players, active_status, bookmaker])
                        
                        # get bet_id to add connections
                        bet_id = get_id(mycursor, BETS_BET_ID, BETS, [BETS_NAME, BETS_OUTCOME, BETS_FULL_INFO, BETS_ODDS], [bet_name, bet_outcome, bet_full_info, bet_odds])
                        
                        if player_id != None:
                            # add to database
                            db_add(db, mycursor, BETS_ASSIGNED, [BETS_ASSIGNED_BET_ID, BETS_ASSIGNED_PLAYER_ID], [bet_id, player_id])
                    
                    # set superbet_scraped to true
                    db_update(db, mycursor, MATCHES, [MATCHES_SUPERBET_SCRAPED], [1], [MATCHES_MATCH_ID], [match_id])

            counter += 1

    elif response.status_code == 404:
        print(f"Code: 404")
    else:
        print("Request failed with status code:", response.status_code)
        
    # Close the cursor and connection
    mycursor.close()
    db.close()


if __name__ == "__main__":
    get_superbet_odds(BOOKMAKER_SUPERBET)