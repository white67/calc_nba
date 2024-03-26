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
            #    if player["player"]["team"]["shortName"].split(" ")[-1] == team_name:
                player_name = player["player"]["name"]
                player_slug = player["player"]["slug"]
                player_sofa_id = player["player"]["id"]
                player_sofascore_link = f"https://www.sofascore.com/player/{player_slug}/{player_sofa_id}"
                player_date_of_birth = player["player"]["dateOfBirthTimestamp"]
                player_date_of_birth = correct_date_timestamp_0h(player_date_of_birth)
                player_country = player["player"]["country"]["name"]
                datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # test
                # print(f"""player_name: {player_name}\n
                #         player_sofascore_link: {player_sofascore_link}\n
                #         player_date_of_birth: {player_date_of_birth}\n
                #         player_country: {player_country}\n
                #         datetime_now: {datetime_now}\n
                #         """)
                
                # test
                update_player_info(db, mycursor, player_name, player_sofascore_link, team_name, player_sofa_id, player_date_of_birth, player_country, datetime_now)
                   
                   
           
        else:
            print("Request failed with status code:", response.status_code)


    # Close the cursor and connection
    mycursor.close()
    db.close()

if __name__ == "__main__":
    update_team_lineup(CFG_HOUR_PRIOR)