from health_ai_digest.digest import PromptBuilder
from health_ai_digest.llm import GroqClient

ARTICLE = """
Title:
Artificial Intelligence for Early Cancer Detection

Abstract:
Artificial intelligence models have shown promising results in improving diagnostic accuracy and reducing false negatives in oncology screening.
"""

def main() -> None:
  prompt_builder = PromptBuilder()

  system_prompt = (
    prompt_builder.build_system_prompt()
  )

  user_prompt = ARTICLE

  client = GroqClient()

  response = client.generate(
    system_prompt=system_prompt,
    user_prompt=user_prompt,
  )

  print("\nSystem Prompt:\n")
  print(system_prompt)  

  print("\nResponse:\n")
  print(response)

if __name__ == "__main__":
  main()
