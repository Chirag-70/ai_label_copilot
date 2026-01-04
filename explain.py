from google import genai
from google.genai import types
import os
import streamlit as st

def explain_ingredients(ingredients_text: str) -> str:
    
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

##percentage of harmful and useful ingredients, means overall rating 
(excellent, good, fair, poor, terrible) and in "%" also

Do NOT exceed 1500 words.
Do NOT give medical advice.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt],
            config=types.GenerateContentConfig(
                max_output_tokens=1500,
                temperature=0.2,
                system_instruction="You're a helpful assistant that explains food ingredients clearly and concisely.You have to give essential information about food ingredients in simple language.You assume that ,the customer/cusumer have not much time to read long and disgusting food label ingredients,they don't know about all ingredients,so you can specify the category of ingredients like preservatives ,sweeteners,artificial colors,flavor enhancers etc and their impact on health in short way.And last point is that you have to give overall rating of food product based on ingredients in percentage and in words like excellent,good,fair,poor,terrible and in percentage also and at last suggest if they can consume it or not.",
                
            )
        )
        return response.text

    except Exception as e:
        return "⚠️ AI service temporarily unavailable. Please try again."


