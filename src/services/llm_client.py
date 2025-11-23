import os
from fastapi import HTTPException

from dotenv import load_dotenv
import requests
import json
from typing import Any

load_dotenv()

def _raise_for_llm_error(response: requests.Response) -> None:
    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail={
                "code": "REQUEST_FAILED",
                "message": f"LLM request failed with message: {response.text}",
            },
        )

def _get_content(response: requests.Response) -> str:
    try:
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise HTTPException(
            status_code=502,
            detail={
                "code": "BAD_RESPONSE",
                "message": "LLM returned an unexpected response format"
            }
        )


class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")
        self.api_url = os.getenv("LLM_API_URL")
        self.model = os.getenv("LLM_MODEL")

    def call_model_json(self, prompt: str) -> dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt},
            ],
            "response_format": {"type": "json_object"},
        }
        response = requests.post(self.api_url, headers=headers, json=payload)

        _raise_for_llm_error(response)

        content = _get_content(response)

        return json.loads(content)

