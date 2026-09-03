import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import create_analysis_prompt


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


ALLOWED_CATEGORIES = [
    "Work",
    "Recruitment",
    "Personal",
    "Finance",
    "Customer Support",
    "Meeting",
    "Other"
]

ALLOWED_PRIORITIES = [
    "Low",
    "Medium",
    "High"
]


def analyze_email(email_text):

    prompt = create_analysis_prompt(email_text)

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You analyze emails and return valid JSON only.",
                temperature=0.2,
                response_mime_type="application/json"
            )
        )

        result = response.text

        data = json.loads(result)

        validated_data = validate_analysis(data)

        return validated_data

    except json.JSONDecodeError:
        raise Exception(
            "The AI returned an invalid JSON response."
        )

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
            f"Unable to analyze the email: {str(e)}"
        )


def validate_analysis(data):

    required_fields = [
        "summary",
        "category",
        "priority",
        "action_required",
        "action_items",
        "deadline"
    ]

    for field in required_fields:

        if field not in data:
            raise Exception(
                f"Missing field in AI response: {field}"
            )

    if data["category"] not in ALLOWED_CATEGORIES:

        data["category"] = "Other"

    if data["priority"] not in ALLOWED_PRIORITIES:

        data["priority"] = "Medium"

    if not isinstance(data["action_required"], bool):

        raise Exception(
            "action_required must be true or false."
        )

    if not isinstance(data["action_items"], list):

        raise Exception(
            "action_items must be a list."
        )

    return data