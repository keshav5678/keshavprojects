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
            "X-Api-Key": "YOUR API KEY ASSOCIATED WITH YOUR API-NINJAS ACCOUNT"
        }
    )
    return resp.json()
