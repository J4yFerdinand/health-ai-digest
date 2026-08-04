import pytest

from health_ai_digest.llm import BaseLLMClient


def test_base_llm_client_cannot_be_instantiated():
    # BaseLLMClient should not be directly instantiated.

    with pytest.raises(TypeError):
        BaseLLMClient()


def test_incomplete_llm_client_cannot_be_instantiated():
    """
    Subclasses that do not implement generate()
    should remain abstract.
    """

    class IncompleteClient(BaseLLMClient):
        pass

    with pytest.raises(TypeError):
        IncompleteClient()


def test_concrete_llm_client_can_generate():
    # Concrete implementations should work correctly.

    class FakeClient(BaseLLMClient):

        def generate(
            self,
            system_prompt: str,
            user_prompt: str,
        ) -> str:
            return "Hello from fake client."

    client = FakeClient()

    response = client.generate(
        system_prompt="system",
        user_prompt="user",
    )

    assert response == "Hello from fake client."
