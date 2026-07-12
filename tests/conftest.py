import pytest

from datetime import datetime, UTC
from collections.abc import Callable

from health_ai_digest.models import (
  Article,
  RankedArticle,
  ArticleSummary,
  SourceType,
  Digest,
)

from health_ai_digest.digest import PromptBuilder

@pytest.fixture
def article_factory() -> Callable[..., Article]:
  # Factory for creating Article instances with sensible defaults.
  def _create_article(
      title: str = "Default Paper",
      url: str = "https://default-paper",
      doi: str | None = None,
      abstract: str | None = "Default abstract.",
      authors: list[str] | None = None,
      keywords: list[str] | None = None,
      published_at=None,
  ) -> Article:
    return Article(
      title=title,
      source=SourceType.PUBMED,
      url=url,
      doi=doi,
      abstract=abstract,
      authors=authors or [],
      keywords=keywords or [],
      published_at=published_at,
    )
  
  return _create_article

@pytest.fixture
def ranked_article_factory(
  article_factory: Callable[..., Article],
  ) -> Callable[..., RankedArticle]:
  # Factory for creating RankedArticle instances.
  def _create_ranked_article(
    score: float = 0.0,
    relevance_score: float = 0.0,
    recency_score: float = 0.0,
    quality_score: float = 0.0,
    **article_kwargs,
  ) -> RankedArticle:

    article=article_factory(**article_kwargs)

    return RankedArticle(
      article=article,
      score=score,
      relevance_score=relevance_score,
      recency_score=recency_score,
      quality_score=quality_score,
    )

  return _create_ranked_article

@pytest.fixture
def article_summary_factory(
  ranked_article_factory: Callable[..., RankedArticle],
  ) -> Callable[..., ArticleSummary]:
  # Factory for creating ArticleSummary instances.
  def _create_article_summary(
    summary: str = "Default summary.",
    key_takeaway: str = "Default key takeaway.",
    **ranked_article_kwargs,
  ) -> ArticleSummary:

    ranked_article = ranked_article_factory(**ranked_article_kwargs)

    return ArticleSummary(
      ranked_article=ranked_article,
      summary=summary,
      key_takeaway=key_takeaway,
    )

  return _create_article_summary

@pytest.fixture
def digest_factory(
  article_summary_factory: Callable[..., ArticleSummary],
  ) -> Callable[..., Digest]:
  # Factory for creating Digest instances.

  def _create_digest(
    generated_at=None,
    articles=None,
  ) -> Digest:
    
    return Digest(
      generated_at=(
        generated_at
        or datetime.now(UTC)
      ),
      articles=(
        articles
        or [article_summary_factory()]
      ),
    )
  
  return _create_digest

@pytest.fixture
def prompt_builder() -> PromptBuilder:
  # PromptBuilder instance.

  return PromptBuilder()

@pytest.fixture
def sample_llm_response() -> str:
  # Mock LLM response.

  return """
Summary:
Researchers developed an AI model that improves cancer detection accuracy.

Key Takeaway:
AI significantly improves diagnostic performance.
""".strip()
