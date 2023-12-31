import requests
import json

V2_EXCHANGE_ENDPOINTS = {
    "mainnet": "https://api.thegraph.com/subgraphs/name/sushiswap/exchange",
}


def fetch_token_prices(token_addresses):
    current_token_price_query_v2 = """
    query tokenPriceQuery($tokenAddress: String!) {
        token(id: $tokenAddress) {
            id
            derivedETH
        }
        bundle(id: "1") {
            ethPrice
        }
    }
"""
    token_prices = {}

    for chain in token_addresses:
        token_prices[chain] = {}
        for token in token_addresses[chain]:
            variables = {"tokenAddress": token}
            result = requests.post(
                V2_EXCHANGE_ENDPOINTS[chain],
                json={"query": current_token_price_query_v2, "variables": variables},
            )

            data = json.loads(result.text)
            token_prices[chain][token] = float(
                data["data"]["token"]["derivedETH"]
            ) * float(data["data"]["bundle"]["ethPrice"])

        return token_prices
