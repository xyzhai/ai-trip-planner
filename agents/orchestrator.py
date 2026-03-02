from langchain_openai import ChatOpenAI
from agents.planner_agent import run_planner
from agents.visa_agent import run_visa_auditor

class Orchestrator:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    def route_request(self, user_input: str, history: list, visa_context: dict):
        """
        Decides which agent to talk to.
        visa_context: {'citizenship': ..., 'residency': ..., 'destination': ...}
        """
        
        # 1. Ask the LLM to classify the intent
        system_msg = (
            "You are a routing assistant. Determine if the user's latest message is "
            "related to 'logistics' (flights/hotels/itinerary) or 'visa' (entry requirements/documents). "
            "Reply with only one word: 'PLANNER' or 'VISA'."
        )
        
        classification = self.llm.predict(f"{system_msg}\n\nUser: {user_input}")

        # 2. Execute the correct agent
        if "VISA" in classification.upper():
            # If we have the context, run the auditor
            if all(visa_context.values()):
                return run_visa_auditor(
                    visa_context['citizenship'], 
                    visa_context['destination'], 
                    visa_context['residency']
                )
            else:
                return "I'd love to check your visa requirements! Please make sure your citizenship and residency are filled in the sidebar."

        else:
            # Run the planner with full history for conversation flow
            response = run_planner(history)
            return response["messages"][-1].content

orchestrator = Orchestrator()