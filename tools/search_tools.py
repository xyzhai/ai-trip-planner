from langchain.tools import tool
from langchain_community.utilities import SerpAPIWrapper
from dotenv import load_dotenv
load_dotenv()
search = SerpAPIWrapper()

@tool
def search_flights(origin: str, destination: str, date: str, cabin_class: str = "Economy"):
    """Searches for real-time flight prices and schedules."""
    query = f"flights from {origin} to {destination} on {date} {cabin_class} class prices"
    return search.run(query)

@tool
def search_hotels(location: str, checkin: str, checkout: str, perks: str = ""):
    """Searches for hotels in a location with specific user benefits or preferences."""
    query = f"best hotels in {location} check-in {checkin} check-out {checkout} {perks}"
    return search.run(query)

@tool
def activity_booking_tool(activity_name: str, city: str, date: str):
    """Checks for museum ticket availability, train times, or activity hours."""
    query = f"{activity_name} in {city} on {date} availability and tickets"
    return search.run(query)