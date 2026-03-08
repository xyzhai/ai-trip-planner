from langchain.tools import tool
import requests
import os
import json


@tool
def get_card_benefits(card_name: str):
    """
    Returns travel benefits, point transfer ratios, and 2026 redemption 
    strategies for specific premium credit cards.
    """
    file_path = os.path.join("data", "wallet.json")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            cards = json.load(f)
    
        key = card_name.lower().strip()
        for card_key in cards:
            if card_key in key:
                return cards[card_key]
    
        return "Card not recognized in wallet."
    except FileNotFoundError:
        return "Error: wallet.json not found in the data directory."
    

def check_award_seats(origin, destination):
    """
    Queries Seats.aero for Business Class Saver awards (under 80k points).
    """
    api_key = os.getenv("SEATS_AERO_KEY")
    # 2026 Partner API Endpoint
    url = f"https://developers.seats.aero/v1/bulk/availability"
    
    headers = {"Partner-Authorization": api_key}
    params = {
        "origin": origin,
        "destination": destination,
        "cabin": "business",
        "max_points": 80000
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("data", [])
    return []