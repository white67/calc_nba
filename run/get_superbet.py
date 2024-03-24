# get current nba odds

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
    
    time.sleep(sleep_random(API_TIMEOUT))
    # get request
    response = requests.get(url_sofa_finished_matches(i), headers=api_headers_sofa)


    # check api status code
    if response.status_code == 200:
        print("Code: 200")
        
        # get all events ids and then parse to api one-by-one
        
    elif response.status_code == 404:
        print(f"Code: 404")
    else:
        print("Request failed with status code:", response.status_code)
        
    # Close the cursor and connection
    mycursor.close()
    db.close()


if __name__ == "__main__":
    get_latest_events()