import json
import os
import ssl
from pathlib import Path

import certifi
import httpx
from dotenv import load_dotenv
from google import genai
from google.genai import types


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")


def _ssl_context() -> ssl.SSLContext:
    """Trust public CAs and certificates installed in the Windows root store."""
    context = ssl.create_default_context(cafile=certifi.where())
    if os.name == "nt":
        for certificate, encoding, trust in ssl.enum_certificates("ROOT"):
            if encoding == "x509_asn" and trust:
                context.load_verify_locations(cadata=certificate)
    return context


client = genai.Client(
    api_key=api_key,
    http_options={
        "httpx_client": httpx.Client(verify=_ssl_context(), timeout=60.0),
        "retry_options": types.HttpRetryOptions(
            attempts=3,
            initialDelay=1,
            maxDelay=5,
            expBase=2,
            jitter=0.2,
            httpStatusCodes=[429, 500, 502, 503, 504],
        ),
    },
)


def generate_reference(question: str) -> dict:
    prompt = f"""
You are an expert university examiner. Generate an expected answer, keywords,
concepts, and a rubric totaling 10 marks for this question.

Return only a JSON object with these keys: expected_answer (string), keywords
(list of strings), concepts (list of strings), and rubric (object whose integer
values total 10).

Question: {question}
"""

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "max_output_tokens": 1500,
            },
        )
        return json.loads(response.text)
    except Exception as exc:
        message = str(exc)
        if "429" in message or "RESOURCE_EXHAUSTED" in message:
            return {
                "error": "Gemini quota is exhausted. Retries were attempted; wait for the quota window to reset or increase the quota for this API key's Google AI Studio project.",
                "error_code": "GEMINI_QUOTA_EXHAUSTED",
            }
        return {"error": message}
