# superbet
def cfg_url_superbet_upcoming(start_date, end_date):
    return f'https://production-superbet-offer-pl.freetls.fastly.net/v2/pl-PL/events/by-date?offerState=prematch&startDate={start_date}&endDate={end_date}'
    # start_date ~ 2024-03-25+17:23:00
    # start_date ~ 2025-03-26+08:00:00

sportId_superbet = 4
tournamentId_superbet = 164
    
def cfg_url_superbet(eventId):
    return f'https://production-superbet-offer-pl.freetls.fastly.net/v2/pl-PL/events/{eventId}?matchIds={eventId}'

def check_player_refers_superbet(specifiers, number):
    # Check if any key starts with "player"
    players_count = sum(1 for key in specifiers if key.startswith('player'))
    
    if number == "single":
        return players_count == 1
    if number == "multiple":
        return players_count > 1

# betclic
def cfg_url_betclic(eventId, categorizationId):
    return f'https://offer.cdn.begmedia.com/api/pub/v6/events/{eventId}?application=2048&categorizationId={categorizationId}&countrycode=pl&language=pa&sitecode=plpa'

categorizationIds = [
    "null",
    30, # top
    22, # wynik
    40, # punkty
    8, # punkty zawodników
    27 # statystyki zawodników
]

# sts
def cfg_url_sts(eventId):
    return f'https://api.sts.pl/web/v1/offer/prematch/{eventId}?lang=pl'

# iforbet
def cfg_url_iforbet(eventId):
    return f'https://www.iforbet.pl/rest/market/events/{eventId}'

###

# sofascore
url_sofa_upcoming_matches = 'https://api.sofascore.com/api/v1/unique-tournament/132/season/54105/events/next/0'

def url_sofa_finished_matches(i):
    return f'https://api.sofascore.com/api/v1/unique-tournament/132/season/54105/events/last/{i}'

def url_sofa_matchpage(eventId):
    return f"https://api.sofascore.com/api/v1/event/{eventId}/lineups"

def url_sofa_playerpage(slug_name, player_id):
    return f"https://www.sofascore.com/player/{slug_name}/{player_id}"