import os
import json
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types
from langdetect import detect

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_flashcards(text):
    # detect language
    try:
        lang = detect(text)
    except:
        lang = "en"

    prompt = f"""
    You are a strict flashcard generator.

    Create at least 15 flashcards from the text below.

    Keep questions simple and clear.
    Keep answers short and precise.
    
    TEXT LANGUAGE: {lang}

    TEXT:
    {text[:2000]}
    """

    try:
        response = client.models.generate_content(
            # model="gemini-flash-latest",
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )

        content = response.text.strip()

        # remove markdown if exists
        content = re.sub(r"```json|```", "", content).strip()

        return json.loads(content)

    except Exception as e:
        print("AI ERROR:", e)
        return [
            {
                "question": "API error",
                "answer": str(e)
            }
        ]