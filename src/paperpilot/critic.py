import json
import os
from pathlib import Path
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def load_prompt(prompt_path: str) -> str:
    """
    Load a prompt file from disk.
    """

    path = Path(prompt_path)

    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    return path.read_text(encoding="utf-8")


def run_critic(
    table_data: Any,
    evidence_data: Any,
    schema: Dict,
    prompt_path: str,
    model: str,
) -> Dict:
    """
    Run the independent critic model.

    Parameters
    ----------
    table_data
        Current extracted comparison table.

    evidence_data
        Supporting evidence associated with the table.

    schema
        Active schema definitions.

    prompt_path
        Path to prompts/critic.md.

    model
        OpenRouter model identifier.

    Returns
    -------
    dict
        Structured critic review.
    """


    if not model.endswith(":free"):
        raise ValueError(
            f"Refusing to use non-free OpenRouter model: {model}"
        )

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise EnvironmentError(
            "OPENROUTER_API_KEY is not set in the environment."
        )

    critic_prompt = load_prompt(prompt_path)

    payload = {
    "model": model,
    "messages": [
        {
            "role": "system",
            "content": critic_prompt,
        },
        {
            "role": "user",
            "content": json.dumps(
                {
                    "schema": schema,
                    "table": table_data,
                    "evidence": evidence_data,
                },
                indent=2,
            ),
        },
    ],
    "temperature": 0.1,
}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload,
        timeout=120,
    )

    response.raise_for_status()

    result = response.json()

    content = result["choices"][0]["message"]["content"]

    try:
        return json.loads(content)

    except json.JSONDecodeError as exc:
        raise ValueError(
            "Critic returned invalid JSON."
        ) from exc