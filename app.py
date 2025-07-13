import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load Groq API key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Streamlit App Title
st.set_page_config(page_title="Cold Email Generator", layout="centered")
st.title("✉️ Cold Email Generator (LLaMA via Groq API)")
st.markdown("Generate cold emails using LLaMA 3 and GenAI")

# User Inputs
name = st.text_input("Your Name")
service = st.text_input("Your Service/Product")
audience = st.text_input("Target Audience")
tone = st.selectbox("Tone of Email", ["Professional", "Friendly", "Casual", "Formal"])
goal = st.text_area("What is the goal of the email?")

# When Button is Clicked
if st.button("Generate Cold Email"):
    if not all([name, service, audience, goal]):
        st.warning("Please fill all fields.")
    else:
        # Create prompt
        prompt = f"""
        You are an expert email writer. Write a cold email with the following:
        - Sender Name: {name}
        - Service: {service}
        - Target Audience: {audience}
        - Tone: {tone}
        - Purpose: {goal}
        """

        # Send API request to Groq
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": prompt}]
        }

        with st.spinner("Generating email..."):
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload
            )
            try:
                generated_email = response.json()["choices"][0]["message"]["content"]
                st.success("Here is your cold email:")
                st.text_area("Generated Email", generated_email, height=300)
            except Exception as e:
                st.error("Something went wrong! Check your API key or internet.")
