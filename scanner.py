from tools.benefit_tools import check_award_seats
from tools.search_tools import search_flights # Your existing SerpApi tool
from tools.notify_tools import send_deal_email

def run_daily_scan():
    report = "<h1>Falcon Daily Travel Report - March 2026</h1>"
    
    # TASK 1: Award Arbitrage (NYC -> Asia/Europe Business)
    long_haul_targets = [("JFK", "TYO"), ("JFK", "IST"), ("LAX", "BKK")]
    report += "<h2>💎 Business Class Award Sweet Spots</h2>"
    for origin, dest in long_haul_targets:
        deals = check_award_seats(origin, dest)
        for deal in deals[:3]: # Top 3
            report += f"<p><b>{origin} -> {dest}</b>: {deal['points']} {deal['source']} points - {deal['date']}</p>"

    # TASK 2: Cash Monitoring (NYC -> London/Paris/Lisbon) - ONE WAY ONLY
    nyc_airports = "JFK,EWR,LGA"
    cash_targets = ["LHR", "CDG", "LIS"]
    report += "<h2>💸 One-Way Cash Deals (Non-stop from NYC)</h2>"
    
    for dest in cash_targets:
        # 'type': '2' signals One-Way to Google Flights API
        params = {
            "departure_id": nyc_airports,
            "arrival_id": dest,
            "outbound_date": "2026-05-15",
            "type": "2", # 1=Round trip, 2=One way
            "stops": "0", # Force non-stop
            "currency": "USD"
        }
        
        results = search_flights(**params)
        
        if results.get('best_flights'):
            best_price = results['best_flights'][0]['price']
            # Target thresholds for one-way deals in 2026
            threshold = 350 if dest in ["LHR", "CDG"] else 400
            
            if best_price < threshold:
                report += f"<p><b>NYC to {dest} (One-Way)</b>: ${best_price} - Non-stop</p>"

    send_deal_email("🚀 New Travel Deals Found!", report)

if __name__ == "__main__":
    run_daily_scan()

## TODO: 1. Scheduling: run on a server
## 2. Verify email in Sendgrid dashboard
## 3. Automation, host this on a platform like render or pythonanywhere