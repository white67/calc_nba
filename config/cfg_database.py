import mysql.connector

MATCHES = "matches"
MATCHES_MATCH_ID = "match_id"
MATCHES_TEAM1 = "team1"
MATCHES_TEAM2 = "team2"
MATCHES_SOFASCORE_LINK = "sofascore_link"
MATCHES_SCRAPED = "scraped"
MATCHES_TEAM1_SCORE = "team2_score"
MATCHES_TEAM2_SCORE = "team2_score"
MATCHES_MATCH_DATE = "match_date"
MATCHES_STADIUM = "stadium"
MATCHES_STADIUM_LOCATION = "stadium_location"

STATS = "stats"
STATS_PLAYER_NAME = "player_name"
STATS_PLAYER_ID = "player_id"
STATS_MATCH_ID = "match_id"

PLAYERS_PLAYER_NAME = "player_name"
PLAYERS_SOFASCORE_LINK = "sofascore_link"
PLAYERS_TEAM = "team"

BETS_NAME = "bet_name"
BETS_OUTCOME = "outcome"
BETS_FULL_INFO = "bet_full_info"
BETS_ODDS = "odds_value"

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
        print("[matches] Insertion successful!")
    except mysql.connector.Error as err:
        print("Error:", err)
        db.rollback()  # Rollback the transaction if an error occurs

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
        print("[stats] Insertion successful!")
    except mysql.connector.Error as err:
        print("Error:", err)
        db.rollback()  # Rollback the transaction if an error occurs

# insert new player
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
        print("[players] Insertion successful!")
    except mysql.connector.Error as err:
        print("Error:", err)
        db.rollback()  # Rollback the transaction if an error occurs

def add_bets_to_database(db, cursor, bet_name, outcome, odds_value, bet_full_info, player_id, match_id, refers_single_player, refers_multiple_players, active_status):
    try:
        cursor.execute("""INSERT INTO bets (
            bet_name,
            outcome,
            odds_value,
            bet_full_info,
            player_id,
            match_id,
            refers_single_player,
            refers_multiple_players,
            active_status
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        );
        """, (bet_name, outcome, odds_value, bet_full_info, player_id, match_id, refers_single_player, refers_multiple_players, active_status))
        
        db.commit()  # Commit the transaction
        print("[bets] Insertion successful!")
    except mysql.connector.Error as err:
        print("Error:", err)
        db.rollback()  # Rollback the transaction if an error occurs


def add_bets_connection(db, cursor, bet_id, player_id):
    try:
        cursor.execute("""INSERT INTO bets_assigned (
            bet_id,
            player_id
        ) VALUES (
            %s, %s
        );
        """, (bet_id, player_id))
        
        db.commit()  # Commit the transaction
        print("[bets_assigned] Insertion successful!")
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

def get_player_id(cursor, columns, data):
    where_clause = " AND ".join(f"{column} = %s" for column in columns)
    
    # Construct the SELECT query
    query = f"SELECT player_id FROM players WHERE {where_clause}"
    
    # Execute the query with the provided data
    cursor.execute(query, data)
    
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

def get_bet_id(cursor, columns, data):
    where_clause = " AND ".join(f"{column} = %s" for column in columns)
    
    # Construct the SELECT query
    query = f"SELECT bet_id FROM bets WHERE {where_clause}"
    
    # Execute the query with the provided data
    cursor.execute(query, data)
    
    # Fetch the result
    result = cursor.fetchone()
    
    # Check if a row was fetched
    if result:
        return result[0]  # Return the player_id
    else:
        return None  # Return None if player_name doesn't exist in the players table
