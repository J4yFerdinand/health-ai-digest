from unittest.mock import MagicMock, patch

import pytest

from health_ai_digest.llm import OpenAIClient

def test_openai_client_requires_api_key(
  monkeypatch,
):
  # OpenAIClient should fail if the API key is not configured.
  monkeypatch.delenv(
    "OPENAI_API_KEY",
    raising=False,
  )

  with pytest.raises(
    ValueError,
  ) as exc_info:
    OpenAIClient()

  assert (
    "OPENAI_API_KEY"
    in str(exc_info.value)
  )

@patch(
  "health_ai_digest.llm.openai.OpenAI"
)
def test_openai_client_initializes(
  mock_openai,
  monkeypatch,
):
  # OpenAIClient should initialize correctly with environment configuration.
  monkeypatch.setenv(
    "OPENAI_API_KEY",
    "fake-api-key",
  )

  monkeypatch.setenv(
    "OPENAI_MODEL",
    "gpt-5-mini",
  )

  client = OpenAIClient()

  assert client._model == "gpt-5-mini"

  mock_openai.assert_called_once_with(
    api_key="fake-api-key",
  )

@patch(
  "health_ai_digest.llm.openai.OpenAI"
)
def test_openai_client_uses_custom_model(
  mock_openai,
  monkeypatch,
):
  # Explicit model parameter should override environment configuration.
  monkeypatch.setenv(
    "OPENAI_API_KEY",
    "fake-api-key",
  )

  monkeypatch.setenv(
    "OPENAI_MODEL",
    "gpt-5-mini",
  )

  client = OpenAIClient(
    model="custom-model",
  )

  assert client._model == "custom-model"

@patch(
  "health_ai_digest.llm.openai.OpenAI"
)
def test_generate_returns_response(
  mock_openai,
  monkeypatch,
):
  # generate() should return the response text from OpenAI.
  monkeypatch.setenv(
    "OPENAI_API_KEY",
    "fake-api-key",
  )

  mock_response = MagicMock()
  mock_response.output_text = (
    "Hello World."
  )

  mock_client = MagicMock()

  mock_client.responses.create.return_value = (
    mock_response
  )

  mock_openai.return_value = (
    mock_client
  )

  client = OpenAIClient()

  response = client.generate(
    system_prompt="system prompt",
    user_prompt="user prompt",
  )

  assert response == "Hello World."

@patch(
  "health_ai_digest.llm.openai.OpenAI"
)
def test_generate_calls_openai_correctly(
  mock_openai,
  monkeypatch,
):
  # generate() should call OpenAI with the expected payload.
  monkeypatch.setenv(
    "OPENAI_API_KEY",
    "fake-api-key",
  )

  mock_response = MagicMock()
  mock_response.output_text = (
    "Hello World."
  )

  mock_client = MagicMock()

  mock_client.responses.create.return_value = (
    mock_response
  )

  mock_openai.return_value = (
    mock_client
  )

  client = OpenAIClient()

  client.generate(
    system_prompt="system prompt",
    user_prompt="user prompt",
  )

  mock_client.responses.create.assert_called_once_with(
    model=client._model,
    input=[
      {
        "role": "system",
        "content": "system prompt",
      },
      {
        "role": "user",
        "content": "user prompt",
      },
    ],
  )
