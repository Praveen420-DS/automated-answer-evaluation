from app.core.gemini import api_key, model_name


print("Model =", model_name)
print("API key configured =", bool(api_key))
print("API key suffix =", api_key[-4:] if api_key else "not configured")
