import sys
import random
sys.path.append('')
import requests
import json
from datetime import datetime, timedelta, timezone

EVENTS_DATE = "2024-04-03"

API_TIMEOUT = 2 # seconds
CFG_HOUR_PRIOR = 22
api_headers_common = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

class bet:
    def __init__(self, team1, team2, btype, name, odds, player, bookmaker, eventId, datetime, scrape_time):
        self.team1 = team1,
        self.team2 = team2,
        self.btype = btype,
        self.name = name,
        self.odds = odds,
        self.player = player,
        self.bookmaker = bookmaker,
        self.eventId = eventId,
        self.datetime = datetime,
        self.scrape_time = scrape_time


# read json file
def read_json_file(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

# save json file
def save_json_file(json_file, data):
    with open(json_file, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False)

def save_json_response(json_file, response):
    data = response.json()
    with open(json_file, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False)
        
def correct_date_timestamp(input_date):
    # Parse the input date string
    input_date = str(datetime.fromtimestamp(input_date, timezone.utc))
    parsed_date = datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S%z")
    
    # needs to convert data 1 hour later, because of the source date being different with UTC +1 / Central European Time (CET)
    new_datetime = parsed_date + timedelta(hours=1)
    print(new_datetime)
    
    # Format the date according to the desired format
    formatted_date = new_datetime.strftime("%Y-%m-%d %H:%M:%S")
    
    return formatted_date

def correct_date_timestamp_0h(input_date):
    # Parse the input date string
    input_date = str(datetime.fromtimestamp(input_date, timezone.utc))
    parsed_date = datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S%z")
    
    # no need to convert data 1 hour later
    new_datetime = parsed_date
    # print(new_datetime)
    
    # Format the date according to the desired format
    formatted_date = new_datetime.strftime("%Y-%m-%d %H:%M:%S")
    
    return formatted_date

def sleep_random(time):
    return random.randint(time*88, time*112)/100