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
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="mansionmusik1400",
        database="nba2024"
    )
    
    # set buffer
    mycursor = db.cursor(buffered=True)
    
    # sleeping before requests
    time.sleep(sleep_random(API_TIMEOUT))
    response = requests.get(url_sofa_upcoming_matches, headers=api_headers_sofa)

    if response.status_code == 200:
        print("Code: 200")
        
        response = response.json()
    
        counter = 0
        for match in response["events"]:
            # get event start time
            match_date = correct_date_timestamp(match["startTimestamp"])

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
            
                team1 = match["homeTeam"]["shortName"]
                team2 = match["awayTeam"]["shortName"]
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
                    add_match_to_database(db, mycursor, team1, team2, sofascore_matchpage_url, scraped, team1_score, team2_score, match_date)
                    print(f"Added match to database.")
    else:
        print("Request failed with status code:", response.status_code)

    
    print(f"Total upcoming matches: {counter}")
    
    # Close the cursor and connection
    mycursor.close()
    db.close()


# match_id, team1, team2, sofascore_link, scraped, team1_score, team2_score, match_date
def add_match_to_database(db, mycursor, team1, team2, sofascore_link, scraped, team1_score, team2_score, match_date):
    try:
        mycursor.execute("""INSERT INTO matches (
            team1,
            team2,
            sofascore_link,
            scraped,
            team1_score,
            team2_score,
            match_date
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s
        );
        """, (team1, team2, sofascore_link, scraped, team1_score, team2_score, match_date))
        db.commit()  # Commit the transaction
        print("Insertion successful!")
    except mysql.connector.Error as err:
        print("Error:", err)
        db.rollback()  # Rollback the transaction if an error occurs
    

# function to check if entry in database (in single table) already exists
def check_duplicate(cursor, table_name, columns, data):
    # Construct the WHERE clause dynamically based on the columns provided
    where_clause = " AND ".join(f"{column} = %s" for column in columns)
    
    # Construct the SELECT query
    query = f"SELECT * FROM {table_name} WHERE {where_clause}"
    
    # Execute the query with the provided data
    cursor.execute(query, data)
    
    # Fetch the results
    result = cursor.fetchone()
    
    # Check if any row was fetched (meaning there's already a duplicate entry)
    return False if result == None else True


if __name__ == "__main__":
    get_new_events(CFG_HOUR_PRIOR)
