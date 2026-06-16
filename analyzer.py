"""The Brain of project - analyzer.py (Gemini approach)"""
import google.generativeai as genai
import os, re, json
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_article(text):
    prompt = f"""
You are a misinformation detection expert.
Analyse this article and return a JSON with:
- trust_score: integer 0-100 (0=completely fake, 100=completely trustworthy)
- explanation: 2-3 sentence summary
- red_flags: list of specific issues found (empty list if none)

Important scoring guide:
- 80-100: Credible, well-sourced news
- 60-79: Mostly reliable with minor issues
- 40-59: Mixed, some unverified claims
- 20-39: Likely misleading
- 0-19: Fake or highly misleading

Article:
{text[:3000]}

Return ONLY a valid JSON object. No markdown, no backticks, no extra text.
Example format:
{{"trust_score": 75, "explanation": "The article...", "red_flags": ["issue1"]}}
"""

    response = model.generate_content(prompt)
    raw = getattr(response, "text", str(response))

    # Debug - print raw response to terminal
    print("RAW RESPONSE:", raw)

    # Strip markdown code blocks if present
    raw = re.sub(r"```json|```", "", raw).strip()

    # Extract JSON object
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        return {
            "trust_score": 50,
            "explanation": "Could not parse response from AI model.",
            "red_flags": []
        }

    try:
        return json.loads(m.group())
    except json.JSONDecodeError:
        return {
            "trust_score": 50,
            "explanation": "AI response was not valid JSON.",
            "red_flags": []
        }
