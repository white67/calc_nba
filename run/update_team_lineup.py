import sys
import time
sys.path.append('')
from config.config import *
from config.cfg_bookmaker import *
from config.cfg_database import *

import mysql.connector

###

# retrieve json file from API and save it to json file
def update_team_lineup(cfg_hour_prior):
    
    # make connection
    db, mycursor = db_connect()
    
    # sleeping before requests
    time.sleep(sleep_random(API_TIMEOUT))
    response = requests.get(url_sofa_team_lineups, headers=api_headers_common)

    if response.status_code == 200:
        print("Code: 200")
        
        response = response.json()
        
        teams_id = {}
    
        counter = 0
        for division in response["standings"]:
            if counter <= 2:
                for team in division["rows"]:
                    teams_id[f"{team["team"]["id"]}"] = team["team"]["shortName"].split(" ")[-1]
    else:
        print("Request failed with status code:", response.status_code)
        
    print(teams_id)
    
    for team_id, team_name in teams_id.items():
        time.sleep(sleep_random(API_TIMEOUT))
        response = requests.get(url_sofa_team_lineup(team_id), headers=api_headers_common)

        if response.status_code == 200:
            print("Code: 200")
            
            response = response.json()
            
            # check if every player's team is updated in database
            for player in response["players"]:
                player_name = player["player"]["name"]
                player_slug = player["player"]["slug"]
                player_sofa_id = player["player"]["id"]
                player_sofascore_link = f"https://www.sofascore.com/player/{player_slug}/{player_sofa_id}"
                if "dateOfBirthTimestamp" in player["player"]:
                    player_date_of_birth = player["player"]["dateOfBirthTimestamp"]
                    player_date_of_birth = correct_date_timestamp_0h(player_date_of_birth)
                else:
                    player_date_of_birth = None
                    # print(f"### BRAK DATY | {player_name} | {player_sofascore_link}")
                if "name" in player["player"]["country"]:
                    player_country = player["player"]["country"]["name"]
                else:
                    country = None
                datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                actual_team = get_id(mycursor, "team", PLAYERS, [PLAYERS_PLAYER_NAME, PLAYERS_SOFASCORE_LINK], [player_name, player_sofascore_link])
                
                if actual_team == None or actual_team != team_name:
                    code = db_update(db, mycursor, PLAYERS, [PLAYERS_PLAYER_NAME, PLAYERS_SOFASCORE_LINK, PLAYERS_TEAM, PLAYERS_SOFASCORE_ID, PLAYERS_BIRTH_DATE, PLAYERS_COUNTRY, PLAYERS_LAST_UPDATE], [player_name, player_sofascore_link, team_name, player_sofa_id, player_date_of_birth, player_country, datetime_now], [PLAYERS_PLAYER_NAME, PLAYERS_SOFASCORE_LINK], [player_name, player_sofascore_link])
                    
                    if code == -2:
                        db_add(db, mycursor, PLAYERS, [PLAYERS_PLAYER_NAME, PLAYERS_SOFASCORE_LINK, PLAYERS_TEAM, PLAYERS_BIRTH_DATE, PLAYERS_SOFASCORE_ID, PLAYERS_COUNTRY, PLAYERS_LAST_UPDATE], [player_name, player_sofascore_link, team_name, player_date_of_birth, player_sofa_id, player_country, datetime_now])

        else:
            print("Request failed with status code:", response.status_code)

    # Close the cursor and connection
    mycursor.close()
    db.close()

if __name__ == "__main__":
    update_team_lineup(CFG_HOUR_PRIOR)
