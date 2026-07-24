import os

from groq import Groq

from health_ai_digest.llm import BaseLLMClient
from health_ai_digest.config.settings import settings

class GroqClient(BaseLLMClient):
  # Client implementation from Groq LLM provider.

  def __init__(
    self,
    model: str | None = None,
  ) -> None:
    
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
      raise ValueError(
        "GROQ_API_KEY environment variable is not configured."
      )
    
    self.model = (
      model
      or settings.groq_model
    )

    self.client = Groq(
      api_key=api_key,
    )

  def generate(
    self,
    system_prompt: str,
    user_prompt: str,
  ) -> str:
    
    response = self.client.chat.completions.create(
      model=self.model,
      messages=[
        {
          "role": "system",
          "content": system_prompt,
        },
        {
          "role": "user",
          "content": user_prompt,
        },
      ],
      temperature=settings.groq_temperature,
      max_completion_tokens=settings.groq_max_tokens,
    )

    if not response.choices:
      raise ValueError(
        "Groq returned no choices."
      )

    content = response.choices[0].message.content

    if not content or not content.strip():
      raise ValueError(
        "Groq returned an empty response."
      )
    
    return content.strip()
  