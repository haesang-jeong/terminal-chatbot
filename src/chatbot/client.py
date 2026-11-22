"""Stateless Gemini Interactions API client (no conversation memory)."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from google import genai

from chatbot.config import ChatbotConfig


def _extract_text_delta(event: Any) -> str | None:
    """Extract text chunk from an Interactions API streaming event."""
    event_type = getattr(event, "event_type", None)
    if event_type not in ("step.delta", "content.delta"):
        return None

    delta = getattr(event, "delta", None)
    if delta is None or getattr(delta, "type", None) != "text":
        return None

    text = getattr(delta, "text", None)
    return text if isinstance(text, str) and text else None


class GeminiChatClient:
    """Minimal stateless wrapper around Gemini Interactions API."""

    def __init__(self, config: ChatbotConfig, *, client: Any | None = None) -> None:
        self._config = config
        self._client = client if client is not None else genai.Client(api_key=config.api_key)

    @property
    def model(self) -> str:
        """Return the configured Gemini model name."""
        return self._config.model

    def send_message_stream(self, message: str) -> Iterator[str]:
        """Send a single independent message without memory and yield text chunks."""
        stream = self._client.interactions.create(
            model=self._config.model,
            input=message,
            store=False,
            stream=True,
        )
        for event in stream:
            chunk = _extract_text_delta(event)
            if chunk is not None:
                yield chunk
