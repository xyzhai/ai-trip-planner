import streamlit as st
from agents.planner_agent import run_planner
from agents.visa_agent import run_visa_auditor

st.set_page_config(page_title="AI Trip Architect", layout="wide")

# --- SIDEBAR: Visa Auditor ---
with st.sidebar:
    st.header("🛂 Quick Visa Check")
    c_ship = st.text_input("Citizenship", placeholder="e.g., China")
    res = st.text_input("Current Residency", placeholder="e.g., USA")
    dest = st.text_input("Destination", placeholder="e.g., Japan")
    
    if st.button("Audit Visa"):
        if all([c_ship, res, dest]):
            with st.spinner("Verifying 2026 rules..."):
                ans = run_visa_auditor(c_ship, dest, res)
                st.success(ans)
        else:
            st.warning("Fill all three fields.")

    st.divider()
    
    # --- ADDED: Card Sidebar ---
    st.header("💳 Wallet & Benefits")
    user_card = st.multiselect(
        "Primary Travel Card:",
        [
            "None", 
            "Chase Sapphire Preferred", 
            "Amex Platinum", 
            "Chase Marriott Bonvoy Boundless", 
            "Citi AAdvantage Platinum Select", 
            "Chase IHG Premier"
        ]
    )

# --- MAIN CHAT ---
st.title("🌍 AI Trip Architect")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Plan my trip..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # In app.py
    chat_history = []
    for m in st.session_state.messages:
        role = "human" if m["role"] == "user" else "ai"
        chat_history.append((role, m["content"]))

    if user_card != "None":
            chat_history.append(("system", f"The user is a {user_card} cardholder. Use 'get_card_benefits' for this card and prioritize its perks in the final plan."))
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # 2. Call agent with the corrected history
            response = run_planner(chat_history)
            
            # In v1.0, agent.invoke returns the full state; 
            # the last message is the answer.
            final_answer = response["messages"][-1].content
            
            st.markdown(final_answer)
            st.session_state.messages.append({"role": "assistant", "content": final_answer})