# superbet
def cfg_url_superbet(eventId):
    return f'https://production-superbet-offer-pl.freetls.fastly.net/v2/pl-PL/events/{eventId}?matchIds={eventId}'

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
url_sofa_matches = 'https://api.sofascore.com/api/v1/unique-tournament/132/season/54105/events/next/0'