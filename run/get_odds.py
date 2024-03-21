import sys
sys.path.append('')
from config.config import *
from config.cfg_bookmaker import *

###

# retrieve json file from API and save it to json file
def get_new_events(cfg_hour_prior):
    response = requests.get(url_sofa_matches, headers=api_headers_sofa)

    if response.status_code == 200:
        print("Code: 200")
        save_json_response("sofascore_upcoming.json", response)
    else:
        print("Request failed with status code:", response.status_code)
    
    response = response.json()
    
    counter = 0
    for match in response["events"]:
        # get event start time
        start_time = datetime.fromtimestamp(match["startTimestamp"], timezone.utc)
        # print(match["startTimestamp"], start_time)
        time_now = datetime.now(timezone.utc)
        time_difference = abs(start_time - time_now)
    
        # Check if the start time is less than 24 hours from now
        time_difference = start_time - time_now
        if timedelta(hours=0) <= time_difference <= timedelta(hours=cfg_hour_prior):
            print(f"{match['homeTeam']['name']} vs {match['awayTeam']['name']}")
            counter += 1
    
    print(f"Total upcoming matches: {counter}")
    
    # return response.json()



if __name__ == "__main__":
    get_new_events(cfg_hour_prior)
