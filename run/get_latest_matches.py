import sys
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
    for i in range(100):
        # get request
        response = requests.get(url_sofa_finished_matches(i), headers=api_headers_sofa)

        # check api status code
        if response.status_code == 200:
            print("Code: 200")
            
            # try to check for indatabase existance for each match in response
            response = response.json()
            
            counter = 0
            for match in response["events"]:
                # get event data saved
                match_date = correct_date_timestamp(datetime.fromtimestamp(match["startTimestamp"], timezone.utc))
                sofascore_matchpage_url = f"https://www.sofascore.com/{match["slug"]}/{match["customId"]}#id:{id}"
                
                # check existance
                entry_exist = check_duplicate(mycursor, MATCHES, [MATCHES_SOFASCORE_LINK, MATCHES_MATCH_DATE], [sofascore_matchpage_url, match_date])
                
                # if entry does not exist
                if not entry_exist:
                    # save data
                    teams = []
                    teams.append(match["homeTeam"]["shortName"])
                    teams.append(match["awayTeam"]["shortName"])
                    scraped = 0
                    team1_score = match["homeScore"]["current"]
                    team2_score = match["awayScore"]["current"]
                    
                    add_match_to_database(teams[0], teams[1], sofascore_matchpage_url, scraped, team1_score, team2_score, match_date)
                    
                    # scrape match_page data -> save to stats table
                    eventId = match["id"]
                    url_sofa_match_stats = url_sofa_matchpage(eventId)
                    
                    get_all_stats(mycursor, url_sofa_match_stats, teams, match_date)
                    
                    
                
                print(f"{match['homeTeam']['name']} vs {match['awayTeam']['name']}")
                counter += 1
            
        elif response.status_code == 404:
            # tbh break already, yeah?
            break
        else:
            print("Request failed with status code:", response.status_code)
        
        response = response.json()
        
    # Close the cursor and connection
    mycursor.close()
    db.close()

# match_id, team1, team2, sofascore_link, scraped, team1_score, team2_score, match_date
def add_match_to_database(mycursor, team1, team2, sofascore_link, scraped, team1_score, team2_score, match_date):

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
    

def get_player_id(cursor, player_name):
    # Execute a SELECT query to retrieve the player_id based on the player_name
    query = "SELECT player_id FROM players WHERE player_name = %s"
    cursor.execute(query, (player_name,))
    
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
def add_stats_to_database(cursor,
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
    
    # find player_id
    player_id = get_player_id(cursor, player_name)
    
    # find match_id
    match_id = get_match_id(cursor, teams, match_date)

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


def get_all_stats(cursor, url_api, teams, match_date):
    response = requests.get(url_api, headers=api_headers_sofa)
    response = response.json()
    
    # for "home" and "away"
    options = ["home", "away"]
    
    i = 0
    for option in options:
        for player in response[option]["players"]:
            name = player["player"]["name"]
            position = player["position"]
            team = teams[options.index(option)]
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
            
            add_stats_to_database(cursor, name,
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
   

if __name__ == "__main__":
    get_latest_events()


# do time.sleep() between api calls
# check if its working with prints