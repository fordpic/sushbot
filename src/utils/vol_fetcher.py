import requests
import json

V2_EXCHANGE_ENDPOINTS = {
    "mainnet": "https://api.thegraph.com/subgraphs/name/sushiswap/exchange",
}


def fetch_token_vol(token_addresses):
    current_token_vol = """
    query tokenVolumeQuery($tokenAddress: String!) {
        token(id: $tokenAddress) {
            volumeUSD
            volume
        }
    }
"""
    current_token_vol = {}
