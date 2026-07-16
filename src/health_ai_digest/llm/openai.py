import os

from openai import OpenAI
from dotenv import load_dotenv

from health_ai_digest.llm import BaseLLMClient

load_dotenv()
class OpenAIClient(BaseLLMClient):
  # OpenAI implementation of BaseLLMClient.

  def __init__(
    self,
    model: str | None = None,
  ) -> None:

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
      raise ValueError(
        "OPENAI_API_KEY environment variable is not configured."
      )

    self._client = OpenAI(
      api_key=api_key,
    )

    self._model = (
      model
      or os.getenv("OPENAI_MODEL")
      or "gpt-5-mini"
    )

  def generate(
    self,
    system_prompt: str,
    user_prompt: str,
  ) -> str:
    # Generate text using OpenAI.
    
    response = self._client.responses.create(
      model=self._model,
      input=[
        {
          "role": "system",
          "content": system_prompt,
        },
        {
          "role": "user",
          "content": user_prompt,
        },
      ],
    )

    return response.output_text.strip()
