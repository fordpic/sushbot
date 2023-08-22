import requests
import json

SUSHI_ENDPOINT = {
    "mainnet": "https://api.thegraph.com/subgraphs/name/olastenberg/sushi",
}


def fetch_total_holders(token_addresses):
    current_holders_query = """
    query totalHoldersQuery {
        sushis {
            userCount
        }
    }
"""

    user_counts = {}

    for chain in token_addresses:
        user_counts[chain] = {}
        for token in token_addresses:
            result = requests.post(
                SUSHI_ENDPOINT[chain],
                json={"query": current_holders_query},
            )

            data = json.loads(result.text)
            user_counts = data["data"]["sushis"][0]["userCount"]

        return user_counts
