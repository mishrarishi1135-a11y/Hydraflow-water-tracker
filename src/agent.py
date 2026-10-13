import os
import time
import certifi

# Conda SSL certificate fix
os.environ['SSL_CERT_FILE'] = certifi.where()

from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def ask_gemini(prompt: str) -> str:
    # Google ke active models dhoondho
    print("Available models check ho rahe hain...")
    available_models = []
    try:
        for m in client.models.list():
            if "generateContent" in (m.supported_actions or []):
                available_models.append(m.name)
    except Exception as e:
        # Fallback list agar list API slow ho
        available_models = ["models/gemini-3.8-flash", "models/gemini-3.8-pro"]

    print(f"Available models: {available_models}")

    # Jo model free ho usse answer lo
    for model_name in available_models:
        try:
            print(f"Connecting to {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text
        except Exception as err:
            print(f"{model_name} par rush hai (503), dusra try kar rahe hain...")
            time.sleep(2)
            continue

        return "Server par temporary overload hai, kripya 1 minute baad run karein."

class WaterIntakeAgent:
    def analyze_intake(self, intake_ml: int) -> str:
        prompt = (
            f"You are a hydration assistant. The user has consumed {intake_ml} ml of water today."
            "Provide hydration status and suggest if they need to drink more water in 2 concise sentences."
        )
        return ask_gemini(prompt)

if __name__ == "__main__":
    prompt = "You are Hydra Flow, an AI water tracking assistant. Introduce yourself in one sentence."
    answer = ask_gemini(prompt)
    print("\n--- Agent Response ---")
    print(answer)