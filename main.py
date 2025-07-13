# main.py

import os
import requests
from dotenv import load_dotenv

# ✅ Load API key from .env file
load_dotenv()
api_key = os.getenv("API_KEY")

# ✅ Check if API key is loaded
if not api_key:
    print("❌ API key not found. Make sure you have an .env file with API_KEY=your_key_here")
    exit()

# ✅ Ask user for inputs
name = input("Enter your name: ")
service = input("What service/product are you offering? ")
audience = input("Who is the target audience? ")
tone = input("What tone do you want? (e.g. professional, friendly): ")
goal = input("What is the goal of the email? ")

# ✅ Create the prompt using inputs
prompt = f"""
You are an expert email writer. Write a cold email with the following:
- Sender Name: {name}
- Service: {service}
- Target Audience: {audience}
- Tone: {tone}
- Purpose: {goal}
"""

# ✅ Prepare headers and payload for Groq API
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "llama3-8b-8192",
    "messages": [
        {"role": "user", "content": prompt}
    ]
}

# ✅ Send POST request to Groq
response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

# ✅ Handle response safely
try:
    response_json = response.json()
    if "choices" in response_json:
        generated_email = response_json["choices"][0]["message"]["content"]
        print("\n📩 Generated Cold Email:\n")
        print(generated_email)
    else:
        print("❌ API did not return 'choices'. Here's what it returned:")
        print(response_json)
except Exception as e:
    print("❌ Failed to parse response:", e)
    print("Raw response:", response.text)
