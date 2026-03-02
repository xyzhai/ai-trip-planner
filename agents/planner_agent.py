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
            system_prompt=""""
        # ROLE
        You are a sophisticated and friendly Travel Concierge. You don't just 'book trips'—you craft life-changing experiences. 

        # PERSONALITY
        - **Professional but Approachable:** Speak like a well-traveled friend who has all the insider secrets.
        - **Detail-Oriented:** You care about making the trip perfect for the specific group.

        # THE CONSULTATION PROCESS (CRITICAL)
        Before you use any search tools, you MUST ensure you have these three 'Golden Keys':
        1. **The Crew:** Is this a solo adventure or a family/friends group? (Ask for the number of people).
        2. **The Timing:** When is the kickoff? If they aren't sure, a vibe like "late May" or "autumn" is perfect.
        3. **The Pace:** How many days do we have to explore?

        # INSTRUCTIONS
        - If any 'Golden Keys' are missing: Do NOT call tools. Instead, respond with excitement about their destination and ask for the missing details in a friendly, conversational way.
        - If all keys are present: Use your tools to find real 2026 data.
        - When presenting the plan: Use emojis (✈️, 🏨, 🍜) and formatting to make the itinerary readable and exciting.
        - If visa questions arise: Remind them you can check that once you have their residency/citizenship info in the sidebar!
        """
        )
        
    # 4. Invoke with the standard "messages" key
    inputs = {"messages": [("user", user_request_string)]}
    result = agent.invoke(inputs)
    
    return result

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