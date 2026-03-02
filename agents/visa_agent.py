from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools.visa_tools import check_visa_requirements

def run_visa_auditor(citizenship: str, destination: str, residency: str):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    agent = create_agent(
        llm,
        tools=[check_visa_requirements],
        system_prompt="""You are a strict Visa Auditor. 
        Provide a ultra-short summary (max 15 words) followed by the official link.
        Examples: 
        - 'Visa Required. Apply at [Link]'
        - 'Visa Free (90 days). Official info: [Link]'
        - 'E-visa Required for residents of {residency}. Link: [Link]'
        - 'Visa free if you hold a valid US/UK visa. Details: [Link]'
        Always prioritize the official government (.gov or embassy) website."""
    )
    
    query = f"Check visa for {citizenship} citizen living in {residency} going to {destination}."
    result = agent.invoke({"messages": [("user", query)]})
    return result["messages"][-1].content