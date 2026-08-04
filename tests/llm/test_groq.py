from unittest.mock import MagicMock, patch

import pytest

from health_ai_digest.config.settings import settings
from health_ai_digest.llm import GroqClient


def test_groq_client_requires_api_key(monkeypatch):
    # GroqClient should fail if the API key is not configured.
    monkeypatch.delenv(
        "GROQ_API_KEY",
        raising=False,
    )

    with pytest.raises(
        ValueError,
        match="GROQ_API_KEY",
    ):
        GroqClient()


@patch("health_ai_digest.llm.groq.Groq")
def test_groq_client_initializes(
    mock_groq_class,
    monkeypatch,
):
    # GroqClient should initializes correctly.
    monkeypatch.setenv(
        "GROQ_API_KEY",
        "fake-api-key",
    )

    client = GroqClient()

    assert client is not None
    assert client.model == settings.groq_model

    mock_groq_class.assert_called_once_with(
        api_key="fake-api-key",
    )


@patch("health_ai_digest.llm.groq.Groq")
def test_generate_returns_response(
    mock_groq_class,
    monkeypatch,
):
    # generate() should return the model response.
    monkeypatch.setenv(
        "GROQ_API_KEY",
        "fake-api-key",
    )

    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(
                content=" Response ",
            )
        )
    ]

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    mock_groq_class.return_value = mock_client

    client = GroqClient()

    response = client.generate(system_prompt="System", user_prompt="User")

    assert response == "Response"


@patch("health_ai_digest.llm.groq.Groq")
def test_generate_calls_groq_correctly(
    mock_groq_class,
    monkeypatch,
):
    # generate() should call Groq SDK correctly.
    monkeypatch.setenv(
        "GROQ_API_KEY",
        "fake-api-key",
    )

    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(
                content=" Response ",
            )
        )
    ]

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    mock_groq_class.return_value = mock_client

    client = GroqClient(
        model="llama-3.1-8b-instant",
    )

    client.generate(
        system_prompt="System prompt",
        user_prompt="User prompt",
    )

    mock_client.chat.completions.create.assert_called_once_with(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "System prompt",
            },
            {
                "role": "user",
                "content": "User prompt",
            },
        ],
        temperature=settings.groq_temperature,
        max_completion_tokens=settings.groq_max_tokens,
    )


@patch("health_ai_digest.llm.groq.Groq")
def test_generate_propagates_sdk_errors(
    mock_groq_class,
    monkeypatch,
):
    # SDK exceptions should propagate.
    monkeypatch.setenv(
        "GROQ_API_KEY",
        "fake-api-key",
    )

    mock_client = MagicMock()

    mock_client.chat.completions.create.side_effect = RuntimeError("SDK failure")

    mock_groq_class.return_value = mock_client

    client = GroqClient()

    with pytest.raises(
        RuntimeError,
        match="SDK failure",
    ):
        client.generate(
            system_prompt="System",
            user_prompt="User",
        )


@patch("health_ai_digest.llm.groq.Groq")
def test_generate_rejects_empty_response(
    mock_groq_class,
    monkeypatch,
):
    # generate() should reject empty responses.
    monkeypatch.setenv(
        "GROQ_API_KEY",
        "fake-api-key",
    )

    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(
                content="  ",
            ),
        ),
    ]

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    mock_groq_class.return_value = mock_client

    client = GroqClient()

    with pytest.raises(
        ValueError,
        match="empty response",
    ):
        client.generate(
            system_prompt="System prompt",
            user_prompt="User prompt",
        )


@patch("health_ai_digest.llm.groq.Groq")
def test_generate_rejects_missing_choices(
    mock_groq_class,
    monkeypatch,
):
    # generate() should reject responses without choices.
    monkeypatch.setenv(
        "GROQ_API_KEY",
        "fake-api-key",
    )

    mock_response = MagicMock()
    mock_response.choices = []

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    mock_groq_class.return_value = mock_client

    client = GroqClient()

    with pytest.raises(
        ValueError,
        match="no choices",
    ):
        client.generate(
            system_prompt="System prompt",
            user_prompt="User prompt",
        )


@patch("health_ai_digest.llm.groq.Groq")
def test_groq_client_uses_custom_model(
    mock_groq_class,
    monkeypatch,
):
    # GroqClient should allow overriding the default model.

    monkeypatch.setenv(
        "GROQ_API_KEY",
        "fake-api-key",
    )

    client = GroqClient(
        model="llama-3.3-70b-versatile",
    )

    assert client.model == "llama-3.3-70b-versatile"

    mock_groq_class.assert_called_once_with(
        api_key="fake-api-key",
    )


@patch("health_ai_digest.llm.groq.Groq")
def test_groq_client_defaults_to_settings_model(
    mock_groq_class,
    monkeypatch,
):
    # Client should use default model from settings.
    monkeypatch.setenv(
        "GROQ_API_KEY",
        "fake-api-key",
    )

    client = GroqClient()

    assert client.model == settings.groq_model
