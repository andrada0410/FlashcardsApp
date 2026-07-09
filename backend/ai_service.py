import os
import json
import re

from dotenv import load_dotenv
from google import genai
from langdetect import detect

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_flashcards(text):
    # detect language from PDF
    try:
        lang = detect(text)
    except:
        lang = "en"

    prompt = f"""
    You are a strict flashcard generator.

    Return ONLY valid JSON.
    Do NOT include markdown.
    Do NOT include extra text.

    Format:
    [
      {{"question": "string", "answer": "string"}}
    ]

    Create 15 flashcards from the text below.

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
        )

        content = response.text.strip()

        # remove markdown if exists
        content = re.sub(r"```json|```", "", content).strip()

        # try direct JSON parse
        try:
            return json.loads(content)
        except:
            pass

        # fallback: extract JSON array only
        start = content.find("[")
        end = content.rfind("]")

        if start != -1 and end != -1:
            try:
                return json.loads(content[start:end + 1])
            except:
                pass

        # final fallback
        return [
            {
                "question": "Parsing error",
                "answer": content
            }
        ]

    except Exception as e:
        print("AI ERROR:", e)
        return [
            {
                "question": "API error",
                "answer": str(e)
            }
        ]