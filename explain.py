from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

from ai_engine.parser import parse_ingredients
from ai_engine.intent import infer_intent
from ai_engine.reasoning import reason_about

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def explain_ingredients(text):
    ingredients = parse_ingredients(text)
    intent = infer_intent(ingredients)
    reasoning = reason_about(ingredients, intent)

    prompt = f"""
You are an AI-native food ingredient copilot.

Ingredients: {ingredients}
User concerns: {intent}
Insights: {reasoning}

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
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=1500,   
                temperature=0.4
                
            )
        )

        return response.text

    except Exception as e:
        print("Gemini Error:", e)  # 🔍 IMPORTANT
        return "⚠️ AI service temporarily unavailable. Please try again."
