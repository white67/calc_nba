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
def get_latest_events():
    
    # make connection
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="mansionmusik1400",
        database="nba2024"
    )
    
    # set buffer
    mycursor = db.cursor(buffered=True)

    # loop thru latest matches until error code, and save those that has not been entered in database yet
    counter = 0
    counter_already_exist = 0
    counter_already_exist_max = 40
    
    # test
    for i in range(0,100):
        # test
        # while True:
        #     check = input("czekam: ")
        #     if check == "c":
        #         break
        
        # sleeping before requests
        time.sleep(sleep_random(API_TIMEOUT))
        # get request
        response = requests.get(url_sofa_finished_matches(i), headers=api_headers_sofa)
        
        print(f"Looping thru page {i+1}...")

        # check api status code
        if response.status_code == 200:
            print("Code: 200")
            
            # try to check for indatabase existance for each match in response
            response = response.json()

            for match in response["events"]:
                
                if counter_already_exist >= counter_already_exist_max:
                    print("\n\n##### Assuming next entries are already scraped, exit...")
                    # Close the cursor and connection
                    mycursor.close()
                    db.close()
                    return 1
                
                print(f"{match['homeTeam']['name']} vs {match['awayTeam']['name']}")
                
                # get event data saved
                match_date = correct_date_timestamp(match["startTimestamp"])
                sofascore_matchpage_url = f"https://www.sofascore.com/{match["slug"]}/{match["customId"]}#id:{match["id"]}"
                
                # check existance
                entry_exist = check_duplicate(mycursor, MATCHES, [MATCHES_SOFASCORE_LINK, MATCHES_MATCH_DATE], [sofascore_matchpage_url, match_date])
                
                teams = []
                teams.append(match["homeTeam"]["shortName"])
                teams.append(match["awayTeam"]["shortName"])
                
                # if entry does not exist
                if not entry_exist:
                    print(f"{counter+1}. Entry does NOT exist. Adding to database ({sofascore_matchpage_url}, {match_date})")
                    
                    # save data
                    scraped = 0
                    team1_score = match["homeScore"]["current"]
                    team2_score = match["awayScore"]["current"]
                    
                    # test
                    add_match_to_database(db, mycursor, teams[0], teams[1], sofascore_matchpage_url, scraped, team1_score, team2_score, match_date)
                else:
                    print(f"{counter+1}.Entry already exist ({sofascore_matchpage_url}, {match_date})")
                    counter_already_exist += 1
                
                # scrape match_page data -> save to stats table
                eventId = match["id"]
                url_sofa_match_stats = url_sofa_matchpage(eventId)
                
                # test
                save_all_stats(db, mycursor, url_sofa_match_stats, teams, match_date)
                
                counter += 1
            
        elif response.status_code == 404:
            print(f"Code: 404")
            # tbh break already, yeah?
            break
        else:
            print("Request failed with status code:", response.status_code)
        
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
    

def get_player_id(cursor, player_name, sofascore_link):
    # Execute a SELECT query to retrieve the player_id based on the player_name
    query = "SELECT player_id FROM players WHERE player_name = %s and sofascore_link = %s"
    cursor.execute(query, (player_name, sofascore_link))
    
    # Fetch the result
    result = cursor.fetchone()
    
    # Check if a row was fetched
    if result:
        return result[0]  # Return the player_id
    else:
        return None  # Return None if player_name doesn't exist in the players table


def get_match_id(cursor, teams, match_date):
    # Execute a SELECT query to retrieve the match_id based on the player_name
    query = "SELECT match_id FROM matches WHERE team1 = %s and team2 = %s and match_date = %s"
    cursor.execute(query, (teams[0], teams[1], match_date))
    
    # Fetch the result
    result = cursor.fetchone()
    
    # Check if a row was fetched
    if result:
        return result[0]  # Return the match_id
    else:
        return None  # Return None if player_name doesn't exist in the players table


# inserting into stats
def add_stats_to_database(db, cursor,
    player_id,
    match_id,
    player_name,
    team,
    teams,
    match_date,
    points,
    rebounds,
    assists,
    minutes_played,
    position,
    free_throws_attempts,
    free_throws_success,
    two_pointers_attempts,
    two_pointers_success,
    three_pointers_attempts,
    three_pointers_success,
    field_goals_attempts,
    field_goals_success,
    rebounds_defensive,
    rebounds_offensive,
    turnovers,
    steals,
    blocks,
    personal_fouls):

    try:
        cursor.execute("""INSERT INTO stats (
            player_id,
            match_id,
            player_name,
            team,
            points,
            rebounds,
            assists,
            minutes_played,
            position,
            free_throws_attempts,
            free_throws_success,
            two_pointers_attempts,
            two_pointers_success,
            three_pointers_attempts,
            three_pointers_success,
            field_goals_attempts,
            field_goals_success,
            rebounds_defensive,
            rebounds_offensive,
            turnovers,
            steals,
            blocks,
            personal_fouls
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        );
        """, (player_id,
        match_id,
        player_name,
        team,
        points,
        rebounds,
        assists,
        minutes_played,
        position,
        free_throws_attempts,
        free_throws_success,
        two_pointers_attempts,
        two_pointers_success,
        three_pointers_attempts,
        three_pointers_success,
        field_goals_attempts,
        field_goals_success,
        rebounds_defensive,
        rebounds_offensive,
        turnovers,
        steals,
        blocks,
        personal_fouls))
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
    
    print(f"query: {query}")
    
    # Execute the query with the provided data
    cursor.execute(query, data)
    
    # Fetch the results
    result = cursor.fetchone()
    
    # Check if any row was fetched (meaning there's already a duplicate entry)
    return False if result == None else True


def add_player_to_database(db, cursor, player_name, sofascore_link, team, birth_date):
    try:
        cursor.execute("""INSERT INTO players (
            player_name,
            sofascore_link,
            team,
            birth_date
        ) VALUES (
            %s, %s, %s, %s
        );
        """, (player_name, sofascore_link, team, birth_date))
        db.commit()  # Commit the transaction
        print("Insertion successful!")
    except mysql.connector.Error as err:
        print("Error:", err)
        db.rollback()  # Rollback the transaction if an error occurs
    

def save_all_stats(db, cursor, url_api, teams, match_date):
    # sleeping before requests
    time.sleep(sleep_random(API_TIMEOUT))
    response = requests.get(url_api, headers=api_headers_sofa)
    
    if response.status_code == 200:
        print("Code: 200")
        response = response.json()
    
        # for "home" and "away"
        options = ["home", "away"]
        
        i = 0
        for option in options:
            for player in response[option]["players"]:
                name = player["player"]["name"]
                team = teams[options.index(option)]
                sofascore_link = url_sofa_playerpage(player["player"]["slug"], player["player"]["id"])
                
                # check if entry already exists based on 3 variables
                player_id = get_player_id(cursor, name, sofascore_link)
                # what if player doesn't exist in database
                if player_id == None:
                    # add a player to database
                    birth_date = correct_date_timestamp(player["player"]["dateOfBirthTimestamp"])
                    add_player_to_database(db, cursor, name, sofascore_link, team, birth_date)
                
                    player_id = get_player_id(cursor, name, sofascore_link)
                    
                    
                match_id = get_match_id(cursor, teams, match_date)
                entry_exist = check_duplicate(cursor, STATS, [STATS_PLAYER_ID, STATS_MATCH_ID], [player_id, match_id])
                
                # if entry does not exist
                if entry_exist:
                    print(f"Player data already inserted ({player_id}, {match_id})")
                    continue
                
                print(f"Addding {name} stats to database...")
                
                position = player["position"]
                stats = player["statistics"]
                
                points = stats["points"]
                rebounds = stats["rebounds"]
                assists = stats["assists"]
                minutes_played = math.floor(stats["secondsPlayed"]/60)
                free_throws_attempts = stats["freeThrowAttempts"]
                free_throws_success = stats["freeThrowsMade"]
                two_pointers_attempts = stats["twoPointAttempts"]
                two_pointers_success = stats["twoPointsMade"]
                three_pointers_attempts = stats["threePointAttempts"]
                three_pointers_success = stats["threePointsMade"]
                field_goals_attempts = stats["fieldGoalAttempts"]
                field_goals_success = stats["fieldGoalsMade"]
                rebounds_defensive = stats["defensiveRebounds"]
                rebounds_offensive = stats["offensiveRebounds"]
                turnovers = stats["turnovers"]
                steals = stats["steals"]
                blocks = stats["blocks"]
                personal_fouls = stats["personalFouls"]
                
                # test
                # print("::", end="")
                # result = ", ".join([
                #     name, position, team, str(points), str(rebounds), str(assists), str(minutes_played),
                #     str(free_throws_attempts), str(free_throws_success), str(two_pointers_attempts),
                #     str(two_pointers_success), str(three_pointers_attempts), str(three_pointers_success),
                #     str(field_goals_attempts), str(field_goals_success), str(rebounds_defensive),
                #     str(rebounds_offensive), str(turnovers), str(steals), str(blocks), str(personal_fouls)
                # ])
                # print(result)
                
                # test
                add_stats_to_database(db, cursor,
                    player_id,
                    match_id,
                    name,
                    team,
                    teams,
                    match_date,
                    points,
                    rebounds,
                    assists,
                    minutes_played,
                    position,
                    free_throws_attempts,
                    free_throws_success,
                    two_pointers_attempts,
                    two_pointers_success,
                    three_pointers_attempts,
                    three_pointers_success,
                    field_goals_attempts,
                    field_goals_success,
                    rebounds_defensive,
                    rebounds_offensive,
                    turnovers,
                    steals,
                    blocks,
                    personal_fouls)   
    elif response.status_code == 404:
        print(f"Code: 404")
        # tbh break already, yeah?
        return 1
    else:
        print("Request failed with status code:", response.status_code)


if __name__ == "__main__":
    get_latest_events()