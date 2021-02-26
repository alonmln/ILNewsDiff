URL_SPORT = "sport"


def validate_change(url: str, old: str, new: str):
    """
    Haaretz sports link look like this `https://www.haaretz.co.il/sport/nba/1.9571478`
    """
    return URL_SPORT not in url
