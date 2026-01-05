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

Respond STRICTLY in JSON format. Do not write anything outside JSON.

Ingredients:
{ingredients_text}

JSON RESPONSE FORMAT:

{{
  "harmful_ingredients_present": "Maltodextrin, Artificial Color, Sodium Benzoate, etc.",

  "harmful_ingredients_percentage": "30% (Safe) / 50% (Moderate) / 70% (Dangerous)",

  "age_groups_should_avoid": {{
    "Children": "0–12 years",
    "Adults": "13–59 years",
    "Senior_Citizens": "60+ years",
    "Pregnant": "Pregnant women"
  }},

  "healthy_ingredients_present": "Whole Grains, Fiber, Vitamins, Minerals, etc.",

  "health_benefits": "Immunity, Digestion, Heart Health, Bone Health, etc.",

  "overall_rating": "Good (70%)"
}}
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


