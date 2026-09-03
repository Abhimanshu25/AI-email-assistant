def create_analysis_prompt(email_text):
    return f"""
You are an AI Email Assistant.

Analyze the email below and return ONLY valid JSON.

Use exactly this format:

{{
    "summary": "short summary",
    "category": "Work | Recruitment | Personal | Finance | Customer Support | Meeting | Other",
    "priority": "Low | Medium | High",
    "action_required": true,
    "action_items": [],
    "deadline": null
}}

Rules:

1. Do not invent information.
2. Choose only one category from the allowed categories.
3. Choose only Low, Medium, or High for priority.
4. action_required must be true or false.
5. action_items must be a list.
6. If there is no deadline, return null.
7. Return ONLY JSON.
8. Keep the summary concise.

EMAIL:

{email_text}
"""


def create_reply_prompt(email_text, analysis, tone):
    return f"""
You are an AI email writing assistant.

Write a reply to the email below.

Tone: {tone}

Use the original email and the analysis as context.

Important rules:

1. Do not invent dates, promises, commitments, or facts.
2. Keep the reply relevant.
3. Write only the email reply.
4. Do not add explanations before or after the reply.

Original Email:

{email_text}

Email Analysis:

{analysis}
"""