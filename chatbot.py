import streamlit as st
import google.generativeai as genai 
import os
from dotenv import load_dotenv 

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Ensure API key is set correctly
if not api_key:
    st.error("⚠️ Gemini API key is missing! Please check your .env file or environment variables.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=api_key)

# Use the correct model name
model = genai.GenerativeModel("gemini-1.5-pro")  # Replace if needed

# Function to read database file
def load_college_data():
    file_path = "college_data.txt"  # Make sure this file exists in the project folder
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    return "No additional college information available."

# Load college data
college_info = load_college_data()

# Streamlit UI
st.title("🎓 College Query Chatbot")
st.write("Ask me anything about the college!")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_query = st.chat_input("Type your question...")

if user_query:
    # Add user query to chat history
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Combine user query with college data for better responses
    prompt = f"User Query: {user_query}\n\nCollege Info:\n{college_info}"

    # Gemini API call
    response = model.generate_content(prompt)

    # Get AI response
    ai_reply = response.text

    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(ai_reply)
