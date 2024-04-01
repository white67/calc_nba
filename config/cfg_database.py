import mysql.connector
from mysql.connector import Error
from datetime import datetime

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWD = "mansionmusik1400"
DB_DATABASE = "nba2024"

MATCHES = "matches"
MATCHES_MATCH_ID = "match_id"
MATCHES_TEAM1 = "team1"
MATCHES_TEAM2 = "team2"
MATCHES_SOFASCORE_LINK = "sofascore_link"
MATCHES_SCRAPED = "scraped"
MATCHES_TEAM1_SCORE = "team1_score"
MATCHES_TEAM2_SCORE = "team2_score"
MATCHES_MATCH_DATE = "match_date"
MATCHES_STADIUM = "stadium"
MATCHES_STADIUM_LOCATION = "stadium_location"

STATS = "stats"
STATS_PLAYER_NAME = "player_name"
STATS_PLAYER_ID = "player_id"
STATS_MATCH_ID = "match_id"
STATS_TEAM = "team"
STATS_P = "points"
STATS_R = "rebounds"
STATS_A = "assists"
STATS_MIN = "minutes_played"
STATS_POS = "position"
STATS_FTA = "free_throws_attempts"
STATS_FTS = "free_throws_success"
STATS_TWO_ATT = "two_pointers_attempts"
STATS_TWO_SUC = "two_pointers_success"
STATS_THREE_ATT = "three_pointers_attempts"
STATS_THREE_SUC = "three_pointers_success"
STATS_FGA = "field_goals_attempts"
STATS_FGS = "field_goals_success"
STATS_RD = "rebounds_defensive"
STATS_RO = "rebounds_offensive"
STATS_TO = "turnovers"
STATS_S = "steals"
STATS_B = "blocks"
STATS_PF = "personal_fouls"

PLAYERS = "players"
PLAYERS_PLAYER_ID = "player_id"
PLAYERS_PLAYER_NAME = "player_name"
PLAYERS_SOFASCORE_LINK = "sofascore_link"
PLAYERS_TEAM = "team"
PLAYERS_BIRTH_DATE = "birth_date"
PLAYERS_SOFASCORE_ID = "sofascore_player_id"
PLAYERS_COUNTRY = "country"
PLAYERS_LAST_UPDATE = "last_update"

BETS = "bets"
BETS_BET_ID = "bet_id"
BETS_NAME = "bet_name"
BETS_OUTCOME = "outcome"
BETS_FULL_INFO = "bet_full_info"
BETS_ODDS = "odds_value"
BETS_BOOKMAKER = "bookmaker"
BETS_PLAYER_ID = "player_id"
BETS_MATCH_ID = "match_id"
BETS_ACTIVE_STATUS = "active_status"
BETS_REFERS_SINGLE = "refers_single_player"
BETS_REFERS_MULTIPLE = "refers_multiple_players"

BETS_ASSIGNED = "bets_assigned"
BETS_ASSIGNED_BET_ID = "bet_id"
BETS_ASSIGNED_PLAYER_ID = "player_id"


# connect with database
def db_connect():
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWD,
        database=DB_DATABASE
    )
    
    # set buffer
    cursor = db.cursor(buffered=True)
    
    return db, cursor

# add to database
def db_add(db, cursor, table_name, columns, data):
    try:
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(columns))
        query = f"""INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders});"""
        cursor.execute(query, data)
        db.commit() 
        print(f"[{table_name}] Insertion successful!")
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


def db_update(db, cursor, table_name, columns, data, columns_to_check, data_to_check):
    try:
        if len(data_to_check) == 0:
            where_clause = ''
            existance = True
        else:
            where_clause = " AND ".join(f"{column} = %s" for column in columns_to_check)
            where_clause = f" WHERE {where_clause}"
            existance = check_duplicate(cursor, table_name, columns_to_check, data_to_check)
            
        if existance:
            updated_str = ', '.join(f"{column} = %s" for column in columns)
            update_query = (f"UPDATE {table_name} SET {updated_str}{where_clause};")
            cursor.execute(update_query, data)
            db.commit()
            print(f"[{table_name}] Entry updated successfully.")
            print(f"{data}")
        else:
            print(f"[{table_name}] Entry does not exist: {data_to_check}")
            # db_add(db, cursor, PLAYERS, [PLAYERS_PLAYER_NAME, PLAYERS_SOFASCORE_LINK, PLAYERS_TEAM, PLAYERS_BIRTH_DATE], [player_name, sofascore_link, team_name, birth_date])
            
            # try adding again
            # here add code but it seems like it needs to be class object
    except mysql.connector.Error as err:
        print("Error:", err)
        db.rollback()  # Rollback the transaction if an error occurs


def get_id(cursor, id_data, table_name, columns, data):
    where_clause = " AND ".join(f"{column} = %s" for column in columns)
    
    # Construct the SELECT query
    query = f"SELECT {id_data} FROM {table_name} WHERE {where_clause}"
    
    cursor.execute(query, data)
    result = cursor.fetchone()
    
    if result:
        return result[0]  # Return the player_id
    else:
        return None  # Return None if player_name doesn't exist in the players table