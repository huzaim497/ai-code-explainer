
import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def explain_code(code: str, language: str, level: str) -> dict:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("Groq API key is missing. Please configure GROQ_API_KEY in .env.")

    client = Groq(api_key=api_key)

    system_prompt = """
    You are an expert programming teacher and code analyst.
    Explain source code clearly according to the requested level.

    Beginner: Use simple language and explain technical terms.
    Advanced: Give a detailed technical explanation.

    Return ONLY a valid JSON object with exactly these fields:
    {
        "summary": "A clear summary of the code",
        "steps": ["First step", "Second step"],
        "suggestions": ["Possible issue or improvement"]
    }

    Do not omit any field. If there are no improvements,
    return an empty suggestions array.
    Do not include Markdown outside JSON.
    """

    user_prompt = f"""
    Programming Language: {language}
    Explanation Level: {level}

    Source Code:
    {code}

    Explain this code using the required JSON structure.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
        max_tokens=1500
    )

    ai_response = response.choices[0].message.content

    if not ai_response:
        raise ValueError("The AI returned an empty response.")

    result = json.loads(ai_response)

    if not isinstance(result, dict):
        raise ValueError("AI returned an invalid response format.")

    result.setdefault("summary", "No summary provided.")
    result.setdefault("steps", [])
    result.setdefault("suggestions", [])

    if not isinstance(result["summary"], str):
        result["summary"] = str(result["summary"])

    if not isinstance(result["steps"], list):
        result["steps"] = [str(result["steps"])]

    if not isinstance(result["suggestions"], list):
        result["suggestions"] = [str(result["suggestions"])]

    return result
