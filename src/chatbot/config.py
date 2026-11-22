"""Configuration loading for the terminal chatbot."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

DEFAULT_MODEL = "gemini-3.1-flash-lite"


class MissingAPIKeyError(ValueError):
    """Raised when GEMINI_API_KEY is not configured."""


@dataclass(frozen=True)
class ChatbotConfig:
    """Runtime settings for the chatbot."""

    api_key: str
    model: str = DEFAULT_MODEL


def load_config(*, dotenv_path: str | None = None) -> ChatbotConfig:
    """Load chatbot configuration from .env and environment variables."""
    load_dotenv(dotenv_path=dotenv_path)

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise MissingAPIKeyError(
            "GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.\n"
            "https://aistudio.google.com/apikey 에서 API 키를 발급받은 뒤 "
            ".env 파일에 GEMINI_API_KEY=... 형태로 입력해 주세요."
        )

    model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL
    return ChatbotConfig(api_key=api_key, model=model)
