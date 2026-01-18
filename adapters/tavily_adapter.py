import os
from tavily import TavilyClient

# =====================================================
# TAVILY ADAPTER (ENGINE)
#
# What this file is:
# - This is NOT the main program
# - This file ONLY knows how to talk to Tavily
#
# What this file does:
# - Takes in a question (string)
# - Asks Tavily to search the web
# - Gives back results in a CLEAN, STANDARD format
#
# VERY IMPORTANT:
# - Every other API adapter must copy THIS structure
# - Same input, same output, different API
# =====================================================

def tavily_query(query: str) -> dict:
    """
    INPUT:
    - query: the question we want to search for

    OUTPUT (ALWAYS this shape):
    {
        "answer": "...",
        "sources": [
            {"title": "...", "url": "..."}
        ]
    }
    """

    # Get the Tavily API key from the environment
    # (this is why we don't hardcode keys in files)
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise RuntimeError("Missing TAVILY_API_KEY")

    # Create the Tavily client (this is the connection)
    client = TavilyClient(api_key=api_key)

    # Ask Tavily to search the web
    result = client.search(
        query=query,
        search_depth="advanced",   # try harder to find a real answer
        max_results=5,
        include_answer=True,
        include_raw_content=False,
    )

    # Pull out sources in a simple format
    sources = []
    for item in result.get("results", []):
        sources.append({
            "title": (item.get("title") or "").strip(),
            "url": (item.get("url") or "").strip(),
        })

    # Try to get Tavily's answer
    answer = (result.get("answer") or "").strip()

    # If Tavily didn't give an answer, we use a fallback
    # (the AI / skill will use the sources later)
    if not answer:
        answer = "No direct answer returned. Use the sources below."

    # IMPORTANT:
    # This return shape is the CONTRACT
    return {
        "answer": answer,
        "sources": sources,
    }
