import os
import requests

# =====================================================
# BRAVE SEARCH ADAPTER
#
# This adapter uses the official Brave Search API.
#
# Docs (for humans):
# https://brave.com/search/api/
#
# The API endpoint below comes directly from Brave's
# developer documentation and example requests.
#
# This file follows the SAME input/output format
# as all other adapters in this project.
# =====================================================

def brave_query(query: str) -> dict:
    """
    INPUT:
    - query (string): the question we want to search

    OUTPUT (standard adapter format):
    {
        "answer": "...",
        "sources": [{"title": "...", "url": "..."}]
    }
    """

    # Read the Brave API key from environment variables
    api_key = os.getenv("BRAVE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing BRAVE_API_KEY")

    # Official Brave Search API endpoint (from docs)
    url = "https://api.search.brave.com/res/v1/web/search"

    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": api_key,
    }

    params = {
        "q": query,
        "count": 5,
    }

    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    # Brave returns results under data["web"]["results"]
    results = (data.get("web") or {}).get("results", [])

    sources = []
    for r in results:
        sources.append({
            "title": (r.get("title") or "").strip(),
            "url": (r.get("url") or "").strip(),
        })

    # Brave does not return a single summarized answer,
    # so we keep a fallback and let the AI combine later.
    answer = "No direct answer returned. Use the sources below."

    return {
        "answer": answer,
        "sources": sources,
    }