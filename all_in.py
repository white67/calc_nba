import time
from run.get_latest_matches import *
from run.get_upcoming_matches import *
from run.update_team_lineup import *
from run.get_superbet_odds import *
from run.get_iforbet_odds import *

if __name__ == "__main__":
    
    # remember to change EVENTS_DATE value: config/config.py
    
    start_time = time.time()
    
    # 1
    get_latest_events()
    
    # 2
    cm = get_new_events(CFG_HOUR_PRIOR)
    
    # 3
    update_team_lineup(CFG_HOUR_PRIOR)
    
    # 4
    cb1 = get_superbet_odds(BOOKMAKER_SUPERBET)
    
    # 5
    cb2 = get_iforbet_odds(BOOKMAKER_IFORBET)
    
    print(f"\n\n")
    print(f"Number of upcoming matches: {cm}")
    print(f"Scraped bets from Superbet: {cb1}")
    print(f"Scraped bets from iForbet: {cb2}")
    
    end_time = time.time()
    print(f"\n\n")
    print(f"Execution time: {end_time - start_time} sec")