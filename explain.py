from google import genai
from google.genai import types
import os
import streamlit as st

def explain_ingredients(ingredients_text: str) -> str:
    # Get API key safely (Cloud + Local)
    api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

    if not api_key:
        return "❌ GOOGLE_API_KEY not found."

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an AI-native food ingredient copilot.

Ingredients:
{ingredients_text}

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
                max_output_tokens=400,
                temperature=0.4
            )
        )
        return response.text

    except Exception as e:
        return "⚠️ AI service temporarily unavailable. Please try again."


