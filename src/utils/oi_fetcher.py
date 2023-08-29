import requests
import json

OI_API_ENDPOINT = "https://api.coinalyze.net/v1/open-interest?symbols="


def fetch_oi(api_key):
    current_oi = {}

    headers = {"api_key": api_key}
    result = requests.get(OI_API_ENDPOINT, headers=headers)

    data = json.loads(result.text)
    print(data)
    current_oi = data

    return current_oi
