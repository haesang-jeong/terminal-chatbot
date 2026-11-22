"""Unit tests for the stateless Gemini terminal chatbot."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from chatbot.client import GeminiChatClient
from chatbot.config import DEFAULT_MODEL, ChatbotConfig, MissingAPIKeyError, load_config


def test_load_config_defaults(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.delenv("GEMINI_MODEL", raising=False)

    empty_env = tmp_path / ".env"
    empty_env.write_text("", encoding="utf-8")

    config = load_config(dotenv_path=str(empty_env))
    assert config == ChatbotConfig(api_key="test-key", model=DEFAULT_MODEL)
    assert config.model == "gemini-3.1-flash-lite"


def test_load_config_custom_model(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

    empty_env = tmp_path / ".env"
    empty_env.write_text("", encoding="utf-8")

    config = load_config(dotenv_path=str(empty_env))
    assert config.model == "gemini-3.1-flash-lite"


def test_load_config_missing_api_key(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    empty_env = tmp_path / ".env"
    empty_env.write_text("", encoding="utf-8")

    with pytest.raises(MissingAPIKeyError):
        load_config(dotenv_path=str(empty_env))


def test_send_message_stream_is_stateless_and_yields_text_only() -> None:
    mock_sdk = MagicMock()
    mock_sdk.interactions.create.side_effect = [
        [
            SimpleNamespace(event_type="interaction.created", interaction=SimpleNamespace(id="id-1")),
            SimpleNamespace(
                event_type="step.delta",
                delta=SimpleNamespace(type="thought_signature", signature="abc"),
            ),
            SimpleNamespace(
                event_type="step.delta",
                delta=SimpleNamespace(type="text", text="안녕"),
            ),
            SimpleNamespace(
                event_type="step.delta",
                delta=SimpleNamespace(type="text", text="하세요!"),
            ),
            SimpleNamespace(event_type="interaction.completed"),
        ],
        [
            SimpleNamespace(
                event_type="step.delta",
                delta=SimpleNamespace(type="text", text="두 번째 응답"),
            ),
        ],
    ]

    chat_client = GeminiChatClient(
        ChatbotConfig(api_key="test-key", model="gemini-3.1-flash-lite"),
        client=mock_sdk,
    )

    first_chunks = list(chat_client.send_message_stream("안녕"))
    second_chunks = list(chat_client.send_message_stream("방금 내가 뭐라고 했지?"))

    assert "".join(first_chunks) == "안녕하세요!"
    assert "".join(second_chunks) == "두 번째 응답"
    assert mock_sdk.interactions.create.call_count == 2

    for call in mock_sdk.interactions.create.call_args_list:
        assert call.kwargs["model"] == "gemini-3.1-flash-lite"
        assert call.kwargs["store"] is False
        assert call.kwargs["stream"] is True
        assert "previous_interaction_id" not in call.kwargs
