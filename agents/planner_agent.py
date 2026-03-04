from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools.search_tools import (
    search_flights,
    search_hotels,
    activity_booking_tool
)

def run_planner(user_request_string: str):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0) # Use mini to save quota
    tools = [search_flights, search_hotels, activity_booking_tool]
    
    agent = create_agent(
            model=llm,
            tools=tools,
            system_prompt="""
            # ROLE
            You are a Travel Logistics & Financial Optimizer. Your goal is to minimize cost while maximizing credit card rewards and safety.

            # OPERATIONAL PROTOCOLS
            1. **Safety First:** Use 'check_safety_score' before planning. If a region is 'CRITICAL' (e.g., March 2026 Middle East conflict), issue a 'SAFETY WARNING' header. Only proceed if the user explicitly insists.
            2. **Missing Data:** Use defaults (1 person, 5 days, +1 month from today) if inputs are vague. Prompt the user for specific requirements only once.
            3. **Visa Logic:** Reference the sidebar visa tool for all entry requirement queries.

            # FINANCIAL & BENEFIT OPTIMIZATION (Nice to have if user ask for it)
            If the user provides a credit card via 'get_card_benefits':
            - **Point Arbitrage:** If cash price > $300, suggest transferring points to partners (e.g., Chase to Hyatt, Amex to Virgin).
            - **Perk Integration:** Apply card-specific hacks (e.g., 4th night free for IHG Premier, baggage savings for Citi AA, $200 FHR credit for Amex Platinum).
            - **2026 Specials:** Explicitly mention March 2026 specific bonuses (e.g., Marriott $100 airline credit).

            # FLIGHT SELECTION HEURISTICS
            - **The 130% Rule:** Compare Non-stop (N) vs. 1-stop (D). If Duration D <= (N * 1.3) and Price(D) < Price(N), prioritize the 1-stop 'Value Pick'.
            - **Business Arbitrage:** If a Business Class route (even 2-stops) is < 1.5x the price of an Economy Non-stop, present it as the 'Luxury Hack'.

            # OUTPUT STRUCTURE
            1. **🚨 Safety Status:** (Only if Critical/Warning)
            2. **✈️ Flight Strategy:** - 'Value Pick' (130% Rule) vs 'Time-Saver' (Non-stop).
            - 'Luxury Hack' (Business deal/Points redemption).
            3. **🏨 Optimized Lodging:** (Prioritize card-benefit hotels like IHG/Marriott/FHR).
            4. **💳 Financial Summary:** Total estimated savings from card perks and point redemptions.
            5. **📍 Itinerary:** High-level daily breakdown.
            """
        )
        
    if isinstance(user_request_string, str):
            # Case 1: Simple string input
            inputs = {"messages": [("human", user_request_string)]}
    else:
            # Case 2: It's the chat history list from your app.py
            inputs = {"messages": user_request_string}
            
    try:
        result = agent.invoke(inputs)
        return result
    except Exception as e:
        # This helps you debug if the structure is still slightly off
        print(f"Agent Invoke Error: {e}")
        raise e

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    query = "Plan a quick 2-day trip to Tokyo from Shanghai. Check flights and a hotel."
    
    try:
        print(f"--- Calling Agent: {query} ---")
        response = run_planner(query)
        
        # 1. Capture the content safely before any stream closes
        if "messages" in response and len(response["messages"]) > 0:
            final_content = response["messages"][-1].content
        else:
            final_content = "No response received."

        # 2. Print with a flush to force it to the screen immediately
        print("\n" + "="*40)
        print("FINAL PLAN:")
        print(final_content)
        print("="*40, flush=True)

    except ValueError as e:
        # If the I/O error happens, we can still see it here
        if "closed file" in str(e):
            # This is a known environmental quirk in some IDEs
            pass 
    except Exception as e:
        print(f"An error occurred: {e}")