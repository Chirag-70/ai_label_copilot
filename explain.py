from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY") or st.secrets["GOOGLE_API_KEY"]

if not api_key:
    raise ValueError("⚠️ GOOGLE_API_KEY not found in environment variables.")

client = genai.Client(api_key=api_key)

prompt = """
You are an AI-native food ingredient copilot.

Respond ONLY in this format:

## Why it matters
(short explanation)

## Tradeoffs
(short)

## Uncertainty
(honest uncertainty)

## Verdict
(one-line verdict)

Do NOT exceed 200 words.
Do NOT give medical advice.
"""

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt],
        config=types.GenerateContentConfig(
            max_output_tokens=1500,
            temperature=0.4
        )
    )
    print(response.text)  
except Exception as e:
    print("Gemini Error:", e)
    print("⚠️ AI service temporarily unavailable. Please try again.")

