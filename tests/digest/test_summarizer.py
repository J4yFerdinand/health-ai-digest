from unittest.mock import MagicMock

import pytest

from health_ai_digest.digest import (
  ArticleSummaryFormatter,
  PromptBuilder,
  Summarizer,
)
from health_ai_digest.models import (
  Article,
  ArticleSummary,
  RankedArticle,
  SourceType,
)

#---------------------------------------------------------------------
# Fixtures
#---------------------------------------------------------------------
@pytest.fixture
def ranked_article():
  article = Article(
    title="AI detects lung cancer",
    source=SourceType.PUBMED,
    url="https://pubmed.ncbi.nlm.nih.gov/12345678/",
    abstract="A study about AI.",
    authors=["John Doe"],
    keywords=["AI", "Cancer"],
  )

  return RankedArticle(
    article=article,
    overall_score=97.5,
    relevance_score=0.95,
    recency_score=0.90,
    quality_score=0.92,
  )

@pytest.fixture
def llm():
  return MagicMock()

@pytest.fixture
def builder():
  mock = MagicMock(spec=PromptBuilder)
  mock.build_prompts.return_value = (
    "SYSTEM PROMPT",
    "USER PROMPT",
  )
  return mock

@pytest.fixture
def formatter(ranked_article):
  mock = MagicMock(spec=ArticleSummaryFormatter)

  mock.parse.return_value = ArticleSummary(
    ranked_article=ranked_article,
    summary="Summary",
    key_takeaway="Key takeaway",
  )

  return mock

#---------------------------------------------------------------------
# Constructor
#---------------------------------------------------------------------
def test_summarizer_initializes(
  llm,
  builder,
  formatter,
):
  summarizer = Summarizer(
    llm_client=llm,
    prompt_builder=builder,
    formatter=formatter,
  )

  assert summarizer._llm is llm
  assert summarizer._prompt_builder is builder
  assert summarizer._formatter is formatter

def test_summarizer_uses_default_prompt_builder(
  llm,
):
  summarizer = Summarizer(
    llm_client=llm,
  )

  assert isinstance(
    summarizer._prompt_builder,
    PromptBuilder,
  )

def test_summarizer_uses_default_formatter(
  llm,
):
  summarizer = Summarizer(
    llm_client=llm,
  )

  assert isinstance(
    summarizer._formatter,
    ArticleSummaryFormatter,
  )

#---------------------------------------------------------------------
# summarize()
#---------------------------------------------------------------------
def test_summarize_calls_prompt_builder(
  ranked_article,
  llm,
  builder,
  formatter,
):
  llm.generate.return_value = "LLM RESPONSE"

  summarizer = Summarizer(
    llm_client=llm,
    prompt_builder=builder,
    formatter=formatter,
  )

  summarizer.summarize(ranked_article)

  builder.build_prompts.assert_called_once_with(
    ranked_article,
  )

def test_summarize_calls_llm(
  ranked_article,
  llm,
  builder,
  formatter,
):
  llm.generate.return_value = "LLM RESPONSE"

  summarizer = Summarizer(
    llm_client=llm,
    prompt_builder=builder,
    formatter=formatter,
  )

  summarizer.summarize(ranked_article)

  llm.generate.assert_called_once_with(
    system_prompt="SYSTEM PROMPT",
    user_prompt="USER PROMPT",
  )

def test_summarize_calls_formatter(
  ranked_article,
  llm,
  builder,
  formatter,
):
  llm.generate.return_value = "LLM RESPONSE"

  summarizer = Summarizer(
    llm_client=llm,
    prompt_builder=builder,
    formatter=formatter,
  )

  summarizer.summarize(ranked_article)

  formatter.parse.assert_called_once_with(
    response="LLM RESPONSE",
    ranked_article=ranked_article,
  )

def test_summarize_returns_formatter_result(
  ranked_article,
  llm,
  builder,
  formatter,
):
  llm.generate.return_value = "LLM RESPONSE"

  expected = formatter.parse.return_value

  summarizer = Summarizer(
    llm_client=llm,
    prompt_builder=builder,
    formatter=formatter,
  )

  result = summarizer.summarize(
    ranked_article,
  )

  assert result is expected

def test_summarize_propagates_llm_errors(
  ranked_article,
  llm,
  builder,
  formatter,
):
  llm.generate.side_effect = RuntimeError(
    "Groq unavailable"
  )

  summarizer = Summarizer(
    llm_client=llm,
    prompt_builder=builder,
    formatter=formatter,
  )

  with pytest.raises(
    RuntimeError,
    match="Groq unavailable",
  ):
    summarizer.summarize(
      ranked_article,
    )
