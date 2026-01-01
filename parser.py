def parse_ingredients(text):
    return [i.strip().lower() for i in text.split(",") if i.strip()]