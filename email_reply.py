import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import create_reply_prompt


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_reply(email_text, analysis, tone):

    prompt = create_reply_prompt(
        email_text,
        analysis,
        tone
    )

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You write helpful and accurate email replies.",
                temperature=0.5
            )
        )

        reply = response.text

        return reply

    except Exception as e:
        error_text = str(e)

        if "API_KEY_INVALID" in error_text or "API key not valid" in error_text:
            raise Exception(
                "The Gemini API key is invalid. Create a key at https://aistudio.google.com/app/apikey and update GEMINI_API_KEY in .env."
            )

        if getattr(e, "status_code", None) == 429 or "RESOURCE_EXHAUSTED" in error_text:
            raise Exception(
                "Gemini free-tier quota is exhausted. Try again later or use another Gemini API key."
            )

        raise Exception(
            f"Unable to generate reply: {str(e)}"
        )