def infer_intent(ingredients):
    intent = []

    if "sugar" in ingredients:
        intent.append("high sugar concern")

    if any(i in ingredients for i in ["sodium benzoate", "msg", "artificial color"]):
        intent.append("additives concern")

    if "palm oil" in ingredients:
        intent.append("fat quality concern")

    return intent