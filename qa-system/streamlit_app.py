# streamlit_app.py
import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Member QA System",
    
    layout="wide"
)

st.title("💬 Member Question Answering System")
st.markdown("Ask natural language questions about member data")

# API endpoint config
# in production this would be the deployed URL
API_URL = st.text_input("API URL", value="http://localhost:8000")

st.markdown("---")

# example questions to help users
st.sidebar.header("Example Questions")
st.sidebar.markdown("""
- When is Layla planning her trip to London?
- How many cars does Vikram Desai have?
- What are Amira's favorite restaurants?
- What activities is Marcus interested in?
""")

# main question input
question = st.text_input(
    "Your Question:",
    placeholder="e.g., When is Layla planning her trip to London?"
)

col1, col2 = st.columns([1, 5])

with col1:
    ask_button = st.button("Ask", type="primary")

with col2:
    refresh_button = st.button("Refresh Data")

# handle refresh
if refresh_button:
    try:
        response = requests.post(f"{API_URL}/refresh", timeout=5)
        if response.status_code == 200:
            st.success("Data cache refreshed!")
        else:
            st.error(f"refresh failed: {response.status_code}")
    except Exception as e:
        st.error(f"error: {e}")

# handle question
if ask_button and question:
    with st.spinner("thinking..."):
        try:
            # call the API
            response = requests.post(
                f"{API_URL}/ask",
                json={"question": question},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "no answer received")
                
                # display the answer nicely
                st.success("Answer:")
                st.markdown(f"**{answer}**")
                
            else:
                st.error(f"API error: {response.status_code} - {response.text}")
                
        except requests.exceptions.Timeout:
            st.error("request timed out - try again")
        except Exception as e:
            st.error(f"error: {e}")

elif ask_button:
    st.warning("please enter a question")

# footer
st.markdown("---")
st.markdown("*Built with FastAPI, OpenAI, and Streamlit*")