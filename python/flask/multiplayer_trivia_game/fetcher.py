from requests import get
from random import choice

def getTrivia(category):
    if category == "all":
        category = choice([
            "artliterature",
            "language",
            "sciencenature",
            "general",
            "fooddrink",
            "peopleplaces",
            "geography",
            "historyholidays",
            "entertainment",
            "toysgames",
            "music",
            "mathematics",
            "religionmythology",
            "sportsleisure"
        ])
    resp = get(
        url="https://api.api-ninjas.com/v1/trivia",
        params={
            "category": category
        },
        headers={
            "X-Api-Key": "P5mzAFmTLRArX5SiMP2hdQ==Tv3ChdEQ6EYrltG8"
        }
    )
    return resp.json()