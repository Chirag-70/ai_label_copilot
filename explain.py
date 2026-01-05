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

Rules:1)Other than json format do not write anything.
2)Only give solution of the food label ingredients ,other than this questions give message to user "Please provide food label ingredients only to explain."
3)Provide real data based on ingredients,don't hallucinate ,don't give wrong information.
4)Show harmful or healthy ingredients mainly 3 to 4 and then write etc.


Ingredients:
{ingredients_text}

Respond ONLY in this format:

Which harmful ingredients are present in the ingredients list?:Example:-Maltodextrin, Artificial Color, Sodium Benzoate ,etc.
the percentage of harmful ingredients in the ingredients list?:Example:-70%(Dangerous) or 30%(Safe) or 50%(Moderate).
gives which age group should avoid this food product?:-Example:-Category is like (Children, Adults, Senior Citizens,pregnant,etc) and also give the specific category age range example:-Children(0-12 years),Adults(13-59 years),Senior Citizens(60+ years),Pregnant.

Healthy ingredients present in the ingredients list?:Example:-Whole Grain, Fiber, Vitamins, Minerals,etc.
it improves health in which factors?:Example:-Immunity, Digestion, Heart Health, Bone Health, etc.

If it contains less than 30% harmful ingredients then consider it as safe to consume otherwise not safe to consume and give other options with similar healthy ingredients.

If it  is safe ,means it contains less than 30% harmful ingredients then wrie it like this:-Good for consumption you can buy it.
If it is not safe ,means it contains more than 30% harmful ingredients then write it like this:-Not good for consumption you should avoid it.

##percentage of harmful and useful ingredients, means overall rating 
(excellent, good, fair, poor, terrible) and in "%" also in one line


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


