import requests
import json

V2_EXCHANGE_ENDPOINTS = {
    "mainnet": "https://api.thegraph.com/subgraphs/name/sushiswap/exchange",
}


def fetch_token_vol(token_addresses):
    current_token_vol_query = """
    query tokenVolumeQuery($tokenAddress: String!) {
        token(id: $tokenAddress) {
            volumeUSD
            volume
        }
    }
"""
    token_vols = {}

    for chain in token_addresses:
        token_vols[chain] = {}
        for token in token_addresses:
            variables = {"tokenAddress:", token}
            result = requests.post(
                V2_EXCHANGE_ENDPOINTS[chain],
                json={"query": current_token_vol_query, "variables": variables},
            )

            data = json.loads(result.text)
            token_vols[chain][token] = data["data"]["token"]["volumeUSD"]

        return token_vols
