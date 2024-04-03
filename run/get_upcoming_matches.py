import sys
import time
sys.path.append('')
from config.config import *
from config.cfg_bookmaker import *
from config.cfg_database import *

import mysql.connector

###

# retrieve json file from API and save it to json file
def get_new_events(cfg_hour_prior):
    
    # make connection
    db, mycursor = db_connect()
    
    # sleeping before requests
    time.sleep(sleep_random(API_TIMEOUT))
    response = requests.get(url_sofa_upcoming_matches, headers=api_headers_common)

    if response.status_code == 200:
        print("Code: 200")
        
        response = response.json()
    
        counter = 0
        for match in response["events"]:
            # get event start time
            match_date = datetime.fromtimestamp(match["startTimestamp"])
            

            input_date = str(datetime.fromtimestamp(match["startTimestamp"], timezone.utc))
            parsed_date = datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S%z")
            
            # needs to convert data 1 hour later, because of the source date being different with UTC +1 / Central European Time (CET)
            new_datetime = parsed_date + timedelta(hours=1)
            time_now = datetime.now(timezone.utc)
            
            # Check if the start time is less than ~24 hours from now
            time_difference = new_datetime - time_now
            
            if timedelta(hours=0) <= time_difference <= timedelta(hours=cfg_hour_prior):
                print(f"{match['homeTeam']['name']} vs {match['awayTeam']['name']}")
                counter += 1
            
                team1 = match["homeTeam"]["shortName"].split(" ")[-1]
                team2 = match["awayTeam"]["shortName"].split(" ")[-1]
                sofascore_matchpage_url = f"https://www.sofascore.com/{match["slug"]}/{match["customId"]}#id:{match["id"]}"
                
                # match_date
                # stadium
                # stadium_location
                
                # check if value of changeTimestamp is 0, then it means that match has not started yet
                # another way to tell match wasn't even possible to be scraped yet is to check current time and compare it to changeTimestamp value, if it's greater that would mean match has ended and it scrapable
                if match["changes"]["changeTimestamp"] == 0:
                    scraped = 0
                    team1_score = 0
                    team2_score = 0
                else:
                    # needs to be scraped
                    team1_score = 0
                    team2_score = 0
                    pass
                
                entry_exist = check_duplicate(mycursor, MATCHES, [MATCHES_SOFASCORE_LINK, MATCHES_MATCH_DATE], [sofascore_matchpage_url, match_date])
                
                if entry_exist:
                    print(f"Entry already exist. skip.")
                else:
                    db_add(db, mycursor, MATCHES, [MATCHES_TEAM1, MATCHES_TEAM2, MATCHES_SOFASCORE_LINK, MATCHES_SCRAPED, MATCHES_TEAM1_SCORE, MATCHES_TEAM2_SCORE, MATCHES_MATCH_DATE], [team1, team2, sofascore_matchpage_url, scraped, team1_score, team2_score, match_date])

    else:
        print("Request failed with status code:", response.status_code)

    print(f"Total upcoming matches: {counter}")
    
    # Close the cursor and connection
    mycursor.close()
    db.close()

if __name__ == "__main__":
    get_new_events(CFG_HOUR_PRIOR)
