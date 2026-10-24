import os
from urllib.parse import quote

import requests
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

# Seconds to wait for another service before giving up
TIMEOUT = 10


# GET an endpoint of the Express/Mongo backend, e.g. "/fetchDealers"
def get_request(endpoint, **kwargs):
    request_url = backend_url + endpoint
    print("GET from {} {}".format(request_url, kwargs))
    try:
        response = requests.get(request_url, params=kwargs, timeout=TIMEOUT)
        return response.json()
    except (requests.RequestException, ValueError) as err:
        print(f"Network exception occurred: {err}")
        return None


# Ask the sentiment microservice: positive, negative or neutral?
def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + quote(text)
    try:
        response = requests.get(request_url, timeout=TIMEOUT)
        return response.json()
    except (requests.RequestException, ValueError) as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return None


# POST a new review to the backend
def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict, timeout=TIMEOUT)
        print(response.json())
        return response.json()
    except (requests.RequestException, ValueError) as err:
        print(f"Network exception occurred: {err}")
        return None
