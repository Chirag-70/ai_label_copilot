import streamlit as st
import os
from explain import explain_ingredients

print("GOOGLE_API_KEY:", os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY"))

st.set_page_config(page_title="AI Food Copilot", layout="centered")

st.title("🧠 AI Food Ingredient Copilot")
st.write("Understand what matters — instantly.")

input_type = st.radio(
    "How would you like to provide ingredients?",
    ["Upload Image", "Paste Ingredients"]
)

ingredients_text = ""

if input_type == "Paste Ingredients":
    ingredients_text = st.text_area(
        "Paste ingredients (comma separated)",
        placeholder="Sugar, Palm Oil, Sodium Benzoate, Artificial Color"
    )

elif input_type == "Upload Image":
    image = st.file_uploader("Upload food label image", type=["jpg", "png"])
    if image:
        
        ingredients_text = "Sugar, Sodium Benzoate, Artificial Color"

if st.button("Explain Ingredients"):
    if ingredients_text.strip():
        with st.spinner("AI is thinking..."):
            result = explain_ingredients(ingredients_text)
        st.markdown(result)
    else:
        st.warning("Please provide ingredients.")

