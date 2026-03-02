import os
from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import tool

search = SerpAPIWrapper()

@tool
def check_visa_requirements(citizenship: str, destination: str, residency: str):
    """
    Finds 2026 visa requirements and official application websites.
    Considers citizenship AND current residency (e.g., green card, BRP).
    """
    query = (f"visa requirements for {citizenship} citizen living in {residency} "
             f"traveling to {destination} 2026 official application website")
    return search.run(query)