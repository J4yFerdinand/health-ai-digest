import pytest

from health_ai_digest.digest.builder import PromptBuilder

@pytest.fixture
def builder():
  return PromptBuilder()

# ======================================================
# build_system_prompt()
# ======================================================
def test_build_system_prompt_returns_string(builder):
  prompt = builder.build_system_prompt()

  assert isinstance(prompt, str)

def test_build_system_prompt_defines_expert_role(builder):
  prompt = builder.build_system_prompt()

  assert "expert medical research analyst" in prompt.lower()

def test_build_system_prompt_contains_guidelines(builder):
  prompt = builder.build_system_prompt()

  assert "Guidelines:" in prompt
  assert "Do not invent facts" in prompt

def test_build_system_prompt_contains_output_format(builder):
  prompt = builder.build_system_prompt()

  assert "Summary:" in prompt
  assert "Key Takeaway:" in prompt
  
def test_build_system_prompr_is_deterministic(builder):
  assert builder.build_system_prompt() == builder.build_system_prompt()

# ======================================================
# build_user_prompt()
# ======================================================

def test_build_user_prompt_returns_string(builder, ranked_article_factory):
  article = ranked_article_factory()

  prompt = builder.build_user_prompt(article)

  assert isinstance(prompt, str)

def test_build_user_prompt_contains_title(builder, ranked_article_factory):
  article = ranked_article_factory(
    title="AI Detects Lung Cancer"
  )

  prompt = builder.build_user_prompt(article)

  assert "AI Detects Lung Cancer" in prompt

def test_build_user_prompt_contains_abstract(builder, ranked_article_factory):
  article = ranked_article_factory(
    abstract="This study evaluates an AI model for cancer detection."
  )

  prompt = builder.build_user_prompt(article)

  assert "This study evaluates an AI model" in prompt

def test_build_user_prompt_contains_keywords(builder, ranked_article_factory):
  article = ranked_article_factory(
    keywords=["AI", "Radiology", "Cancer"]
  )

  prompt = builder.build_user_prompt(article)

  assert "AI" in prompt
  assert "Radiology" in prompt
  assert "Cancer" in prompt

def test_build_user_prompt_contains_metadata(builder, ranked_article_factory):
  article = ranked_article_factory(
    title="Medical AI",
    doi="10.1234/test-doi",
    authors=["Alice", "Bob"],
  )

  prompt = builder.build_user_prompt(article)

  assert "10.1234/test-doi" in prompt
  assert "Alice" in prompt
  assert "Bob" in prompt

# ======================================================
# build()
# ======================================================
def test_build_combines_system_and_user_prompts(
  builder,
  ranked_article_factory,
):

  article = ranked_article_factory()

  prompt = builder.build(article)

  assert builder.build_system_prompt() in prompt
  assert builder.build_user_prompt(article) in prompt

def test_build_returns_string(builder, ranked_article_factory):
  article = ranked_article_factory()

  prompt = builder.build(article)

  assert isinstance(prompt, str)

def test_build_is_deterministic(builder, ranked_article_factory):
  article = ranked_article_factory()

  assert builder.build(article) == builder.build(article)
