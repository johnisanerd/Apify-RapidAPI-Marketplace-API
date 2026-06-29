"""RapidAPI Marketplace API - Python quick-start example.

This example calls the RapidAPI Marketplace API on Apify, which searches the
RapidAPI marketplace and returns structured data about each API: pricing,
category, popularity score, latency, success rate, publisher, billing plans
and ratings. No RapidAPI account is required.

Actor landing page: https://apify.com/johnvc/rapidapi-marketplace-api?fpr=9n7kx3
Get a free Apify API key: https://apify.com?fpr=9n7kx3

Setup (uv only, never pip):
    curl -LsSf https://astral.sh/uv/install.sh | sh   # if uv is not installed
    uv sync
    cp .env.example .env        # then paste your APIFY_API_TOKEN into .env
    uv run python rapidapi-marketplace-api-example.py
"""

import os

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("APIFY_API_TOKEN")
if not API_TOKEN:
    raise SystemExit(
        "Set APIFY_API_TOKEN in your environment or .env file. "
        "Get a free token at https://apify.com?fpr=9n7kx3"
    )

client = ApifyClient(API_TOKEN)

# Inputs are kept small (maxResults=5, one search term) to keep this first run
# inexpensive. Raise these once you know your budget. The marketplace caps a
# single search at 1000 results; use multiple search terms to gather more.
run_input = {
    "searchTerms": ["weather"],          # one or many keywords, each searched separately
    "category": "Weather",               # optional single category filter
    "sortBy": "ByTrending",              # ByRelevance | ByTrending | ByUpdatedAt | ByAlphabetical
    "order": "DESC",                     # ASC | DESC
    "maxResults": 5,                     # per search term; small for a cheap first run
    "detailedInfo": False,               # True adds billing plans, ratings, readme (extra fetch)
    # "listingUrls": [                    # optionally extract specific API pages directly
    #     "https://rapidapi.com/apidojo/api/yahoo-finance1"
    # ],
}

print("Running the RapidAPI Marketplace API...")
run = client.actor("johnvc/rapidapi-marketplace-api").call(run_input=run_input)

if run is None:
    raise SystemExit("The Actor run did not return a result.")

items = list(client.dataset(run.default_dataset_id).iterate_items())
print(f"Returned {len(items)} API listing(s).\n")

# Show a few key fields from each result.
for item in items:
    if item.get("result_type") == "error":
        print(f"  ! {item.get('error_message')}")
        continue
    print(f"- {item.get('name')}  [{item.get('pricing')}]  category={item.get('category')}")
    print(f"    popularity={item.get('popularityScore')}  "
          f"success={item.get('avgSuccessRate')}%  latency={item.get('avgLatency')}ms")
    print(f"    by {item.get('publisher')}  ->  {item.get('url')}")
