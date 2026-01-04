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
Strictly follow json format.
Use simple/casual language that a general consumer can easily understand.

Ingredients:
{ingredients_text}

Respond ONLY in this format:

## Why it matters
(short explanation) in 1-2 lines

## Sacrifices
(short) in 1-2 lines

## Uncertainty
(honest uncertainty) in 1-2 lines

## Decision
(one-line verdict) in 1 line

##percentage of harmful and useful ingredients, means overall rating 
(excellent, good, fair, poor, terrible) and in "%" also in one line

example:if user provide ingredients of healthy and unhealthy food then response will be like this
:->First share healthy food ingredients response then unhealthy food ingredients response in 1-2 lines.
-->then analyse and apply your reasoning in 1-2 lines.
-->finally give overall rating in % and words in one line.


Do NOT exceed 2000 words.
Do NOT give medical advice.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt],
            config=types.GenerateContentConfig(
                max_output_tokens=2000,
                temperature=0.2,
                system_instruction="You are a helpful assistant who explains food ingredients clearly and concisely. Your task is to provide essential information about food ingredients in simple language. You should assume that consumers do not have much time to read long and confusing food labels and may not be familiar with all ingredients. Therefore, categorize the ingredients (such as preservatives, sweeteners, artificial colors, flavor enhancers, etc.) and briefly explain their impact on health.Finally, give an overall rating of the food product based on its ingredients, expressed both as a percentage and in words (Excellent, Good, Fair, Poor, or Terrible). At the end, suggest whether the product is suitable for consumption or not.Main point is that give maximum two lines answer/solution according to content prompt which i given.",
                
            )
        )
        return response.text

    except Exception as e:
        return "⚠️ AI service temporarily unavailable. Please try again."


