import os

from ollama import Client

from health_ai_digest.llm import BaseLLMClient


class OllamaClient(BaseLLMClient):
    # Local LMM client powered by Ollama.

    def __init__(
        self,
        model: str | None = None,
        host: str | None = None,
    ):
        self.model = model or os.getenv("OLLAMA_MODEL") or "llama3.1:8b"

        self.host = host or os.getenv("OLLAMA_HOST") or "http://localhost:11434"

        self.client = Client(host=self.host)

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self.client.generate(
            model=self.model,
            prompt=prompt,
        )

        return response["response"].strip()
