

from typing import Union
from enum import Enum
import json

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests


headers = {
    "User-Agent":
    "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/101.0",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
}
reviews_headers = {
    "User-Agent":
    "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json",
    "Upgrade-Insecure-Requests": "1",
    "TE": "trailers"
}


def get_user_data(username: str):
    """
    Get basic seller details and CSRF Token
    """
     # try: 
    session = requests.Session()
    seller_url = f"https://www.fiverr.com/{username}"
    data = session.get(seller_url, headers=headers)
    soup = BeautifulSoup(data.text, "lxml")
    # print(soup.find("script", id="perseus-initial-props").get_text())
    seller_data = json.loads(soup.find("script", id="perseus-initial-props").string or "null")
    seller_data["csrfToken"] = soup.find("meta", {"property": "csrfToken"}).get("content")
    return session, seller_data
    # except Exception:
    ''' 
        print("ERROR")
        
        print(data)
        print(data.text)
        print(soup.find("script", id="perseus-initial-props"))
        
        return "hi" , "hello"

'''





"""
Get seller reviews
"""
limit = 50
username = "flugcraft"

session, user_data = get_user_data(username)
url = f"https://www.fiverr.com/reviews/user_page/fetch_user_reviews/{user_data['userData']['user']['id']}"

# Adding CSRF Token
reviews_headers["X-CSRF-Token"] = user_data["csrfToken"]
reviews_headers["Referer"] = f"https://www.fiverr.com/flugcraft"
    # return user_data["csrfToken"]
    # Setting up payload
payload: dict[str, str] = {}
payload["user_id"] = user_data["userData"]["user"]["id"]
payload["limit"] = "500"
reviews: list[dict[str, str]] = []
while True:
    data = session.get(url, headers=headers, params=payload)
    data = data.json()
    reviews.extend(data["reviews"])
    if not data["has_next"] or len(reviews) >= limit:
        break
    payload["last_star_rating_id"] = reviews[-1]["id"]
    payload["last_review_id"] = reviews[-1]["id"]
reviews = reviews[:limit]


with open('data.json', 'w') as fp:
        pl_d = json.dumps(reviews)
        fp.write(pl_d)
        # print(pl_d)