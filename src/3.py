

from pickletools import read_int4
from typing import Union
from enum import Enum
import json

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://fiverr.com/flugcraft"

payload={}
headers = {
    "User-Agent":
    "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/101.0",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
}

response = requests.request("GET", url, headers=headers, data=payload)

soup = BeautifulSoup(response.text, "html.parser")

token = soup.find("meta", {"property": "csrfToken"}).get("content")
print(token)




url2 = "https://www.fiverr.com/reviews/user_page/fetch_user_reviews/82095660?user_id=82095660&limit=50"

payload2={}
headers2= {
    "User-Agent":
    "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json",
    "Upgrade-Insecure-Requests": "1",
    "TE": "trailers",
    "X-CSRF-Token": token
}

response2 = requests.request("GET", url2, headers=headers2, data=payload2)

textraw = response2.text

with open('data.json', 'w') as fp:
        fp.write(response2.text)

amount_index = textraw.find('"total_count":')

amount = textraw[amount_index+14:-1]

text = textraw.replace('{"reviews":','')
text = text.replace(',"has_next":false,"total_count":31}','')
print(amount)
b = 0
for i in range(int(amount)):
    a = text.find('"id":"', b )
    text = text[:a+6] + str(i) + text[a+6+24:]
    b = a + 3


with open('data.json', 'w') as fp:
        fp.write(text)


pdObj = pd.read_json('data.json', orient='index')
csvData = pdObj.to_csv(index=False)

with open('data.csv', 'w') as fp:
        fp.write(csvData)