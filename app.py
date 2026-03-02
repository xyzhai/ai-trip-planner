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

    chat_history = [(m["role"], m["content"]) for m in st.session_state.messages]

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Call agent with full history
            response = run_planner(chat_history)
            final_answer = response["messages"][-1].content
            
            st.markdown(final_answer)
            st.session_state.messages.append({"role": "assistant", "content": final_answer})