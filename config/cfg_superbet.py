import sys
import time
sys.path.append('')
from config.config import *
from config.cfg_bookmaker import *
from config.cfg_database import *

def wrong_team_name(team):
    if team.lower() == "washington":
        return "Wizards"
    return team

def convert_bet_name(bet_name):
    stat_name = []
    
    if bet_name.replace(" ", "") == "Liczba punktów zawodnika (z dogrywką)".replace(" ", ""):
        stat_name.append(STATS_P)
        return stat_name
    
    if bet_name.replace(" ", "") == "Liczba asyst zawodnika (z dogrywką)".replace(" ", ""):
        stat_name.append(STATS_A)
        return stat_name
    
    if bet_name.replace(" ", "") == "Liczba zbiórek zawodnika (z dogrywką)".replace(" ", ""):
        stat_name.append(STATS_R)
        return stat_name
    
    if bet_name.replace(" ", "") == "Liczba trafionych rzutów za 3 punkty zawodnika (z dogrywką)".replace(" ", ""):
        stat_name.append(STATS_THREE_SUC)
        return stat_name
    
    if bet_name.replace(" ", "") == "Liczba przechwytów zawodnika (z dogrywką)".replace(" ", ""):
        stat_name.append(STATS_S)
        return stat_name
    
    if bet_name.replace(" ", "") == "Liczba strat zawodnika (z dogrywką)".replace(" ", ""):
        stat_name.append(STATS_TO)
        return stat_name
    
    if bet_name.replace(" ", "") == "Liczba bloków zawodnika (z dogrywką)".replace(" ", ""):
        stat_name.append(STATS_B)
        return stat_name
    
    if bet_name.replace(" ", "") == "Liczba punktów i asyst zawodnika (z dogrywką)".replace(" ", ""):
        stat_name.append(STATS_P)
        stat_name.append(STATS_A)
        return stat_name
    
    if bet_name.replace(" ", "") == "Liczba punktów i zbiórek zawodnika (z dogrywką)".replace(" ", ""):
        stat_name.append(STATS_P)
        stat_name.append(STATS_R)
        return stat_name
    
    if bet_name.replace(" ", "") == "Liczba asyst  i zbiórek zawodnika (z dogrywką)".replace(" ", ""):
        stat_name.append(STATS_A)
        stat_name.append(STATS_R)
        return stat_name
    
    if bet_name.replace(" ", "") == "Liczba przechwytów i bloków zawodnika (z dogrywką)".replace(" ", ""):
        stat_name.append(STATS_S)
        stat_name.append(STATS_B)
        return stat_name
    
    if bet_name.replace(" ", "") == "Liczba punktów, asyst i zbiórek zawodnika (z dogrywką)".replace(" ", ""):
        stat_name.append(STATS_P)
        stat_name.append(STATS_A)
        stat_name.append(STATS_R)
        return stat_name
    
    if bet_name.replace(" ", "") == "Liczba trafionych rzutów z gry (z dogrywką)".replace(" ", ""):
        stat_name.append(STATS_FGS)
        return stat_name
    
    if bet_name.replace(" ", "") == "Liczba oddanych rzutów z gry  (z dogrywką)".replace(" ", ""):
        stat_name.append(STATS_FGA)
        return stat_name
    
    if bet_name.replace(" ", "") == "Liczba oddanych rzutów wolnych zawodnika (z dogrywką)".replace(" ", "") or bet_name.replace(" ", "") == "Liczba rzutów wolnych zawodnika (z dogrywką)".replace(" ", ""):
        stat_name.append(STATS_FTA)
        return stat_name
    
    if bet_name.replace(" ", "") == "Liczba trafionych rzutów wolnych zawodnika (z dogrywką)".replace(" ", ""):
        stat_name.append(STATS_FTS)
        return stat_name
    
    if bet_name.replace(" ", "") == "Liczba rzutów za 2pkt zawodnika (z dogrywką)".replace(" ", ""):
        stat_name.append(STATS_TWO_ATT)
        return stat_name
    
    if bet_name.replace(" ", "") == "Liczba trafionych rzutów za 2pkt zawodnika (z dogrywką)".replace(" ", ""):
        stat_name.append(STATS_TWO_SUC)
        return stat_name
    
    if bet_name.replace(" ", "") == "Double double (z dogrywką)".replace(" ", ""):
        # stat_name.append("dd")
        return None
    
    if bet_name.replace(" ", "") == "Triple double (z dogrywką)".replace(" ", ""):
        # stat_name.append("td")
        return None
    
    return None
    
    # if bet_name == "1.kwarta - Liczba punktów zawodnika":
    #     stat_name.append()
    #     return stat_name
    
    # if bet_name == "1.kwarta - Liczba asyst zawodnika":
    #     stat_name.append()
    #     return stat_name
    
    # if bet_name == "1.kwarta - Liczba zbiórek zawodnika":
    #     stat_name.append()
    #     return stat_name
