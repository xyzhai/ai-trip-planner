from langchain.tools import tool
from langchain_community.utilities import SerpAPIWrapper
import json

search = SerpAPIWrapper()

@tool
def retrieve_official_benefits(card_name: str, country: str = "US"):
    """
    Searches for the official benefit terms and current perks for a specific credit card.
    Use this to get real-time info like 'current statement credits' or 'travel insurance limits'.
    """
    # Specific query to find official PDFs or terms pages
    query = f"official {card_name} {country} guide to benefits site:americanexpress.com OR site:chase.com OR site:capitalone.com"
    
    raw_results = search.run(query)
    
    # We return the search results; the LLM (GPT-4o) is excellent at 
    # reading these snippets and extracting the current perks.
    return f"Latest benefits found for {card_name}:\n{raw_results}"

@tool
def check_user_wallet():
    """Returns the list of cards the user actually owns from local data."""
    try:
        with open("data/user_wallet.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return "No wallet found. User should add cards first."