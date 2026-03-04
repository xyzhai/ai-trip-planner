from langchain.tools import tool

@tool
def get_card_benefits(card_name: str):
    """
    Returns travel benefits, point transfer ratios, and 2026 redemption 
    strategies for specific premium credit cards.
    """
    CARDS = {
        "Chase Sapphire Preferred": {
            "transfer_partners": ["Hyatt (1:1 - Best Value)", "United (1:1)", "Southwest (1:1)", "British Airways (1:1)"],
            "redemption_val": "1.25 cents per point via Chase Travel Portal",
            "perks": ["$50 Annual Hotel Credit", "10% Anniversary Points Boost", "Primary Rental Car Insurance"],
            "strategy": "Transfer to Hyatt for high-end stays; use Portal for cheap domestic flights."
        },
        "Amex Platinum": {
            "transfer_partners": ["Delta (1:1)", "Hilton (1:2)", "Virgin Atlantic (1:1)", "Flying Blue (1:1)"],
            "redemption_val": "Best value via airline transfers; poor portal value.",
            "perks": ["$200 Hotel Credit (FHR/HC)", "$200 Airline Fee Credit", "Centurion Lounge Access", "Clear Plus Credit"],
            "strategy": "Book 'Fine Hotels + Resorts' to use the $200 credit and get free breakfast/late checkout."
        },
        "Chase Marriott Bonvoy Boundless": {
            "loyalty_program": "Marriott Bonvoy",
            "perks": ["Annual Free Night (up to 35k points)", "15 Elite Night Credits", "Silver Elite Status", "5 Free Nights"],
            "special_2026_offer": "$100 Airline Statement Credit ($50 semi-annually) available through Dec 2026.",
            "strategy": "Spend $250 on airfare before June 30 to trigger the first $50 credit."
        },
        "Citi AAdvantage Platinum": {
            "loyalty_program": "American Airlines AAdvantage",
            "perks": ["First Checked Bag Free (Domestic)", "Preferred Boarding", "25% In-flight Food/Drink Discount"],
            "special_2026_offer": "80,000 Mile Sign-up Bonus active for March 2026.",
            "strategy": "Use for domestic AA flights to save on baggage fees (approx $70 round-trip for two)."
        },
        "Chase IHG Premier": {
            "loyalty_program": "IHG One Rewards",
            "perks": ["4th Night Free on Point Redemptions", "Annual Free Night (up to 40k points)", "Automatic Platinum Elite"],
            "redemption_hack": "You can 'top off' the 40k Free Night with extra points for luxury InterContinental stays.",
            "strategy": "Always book in 4-night increments to maximize the 25% points discount."
        }
    }
    
    key = card_name.lower().strip()
    for card_key in CARDS:
        if card_key in key:
            return CARDS[card_key]
    
    return "Card not recognized. Please select from Chase, Amex, Citi, or Marriott/IHG co-brands."