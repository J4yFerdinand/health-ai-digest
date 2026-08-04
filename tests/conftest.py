from collections.abc import Callable
from datetime import UTC, datetime

import pytest

from health_ai_digest.digest import PromptBuilder
from health_ai_digest.models import (
    Article,
    ArticleSummary,
    Digest,
    RankedArticle,
    SourceType,
)

DEFAULT_ARTICLE_TITLE = "Default Paper"
DEFAULT_ARTICLE_URL = "https://default-paper"
DEFAULT_ABSTRACT = "Default abstract."
DEFAULT_SUMMARY = "Default summary."
DEFAULT_KEY_TAKEAWAY = "Default key takeaway."


@pytest.fixture
def article_factory() -> Callable[..., Article]:
    # Factory for creating Article instances with sensible defaults.
    def _create_article(
        title: str = DEFAULT_ARTICLE_TITLE,
        url: str = DEFAULT_ARTICLE_URL,
        doi: str | None = None,
        abstract: str | None = DEFAULT_ABSTRACT,
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

        article = article_factory(**article_kwargs)

        return RankedArticle(
            article=article,
            overall_score=score,
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
        summary: str = DEFAULT_SUMMARY,
        key_takeaway: str = DEFAULT_KEY_TAKEAWAY,
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
        generated_at: datetime | None = None,
        articles: list[ArticleSummary] | None = None,
    ) -> Digest:

        return Digest(
            generated_at=(generated_at or datetime.now(UTC)),
            articles=(articles or [article_summary_factory()]),
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


@pytest.fixture
def fixed_datetime() -> datetime:
    return datetime(
        2026,
        1,
        15,
        12,
        0,
        0,
        tzinfo=UTC,
    )


@pytest.fixture
def invalid_llm_response() -> str:
    return """
Invalid response.
No expected format.
""".strip()


@pytest.fixture
def article_summaries(
    article_summary_factory,
) -> list[ArticleSummary]:

    return [
        article_summary_factory(
            summary="Summary 1",
            key_takeaway="Takeaway 1",
        ),
        article_summary_factory(
            summary="Summary 2",
            key_takeaway="Takeaway 2",
        ),
        article_summary_factory(
            summary="Summary 3",
            key_takeaway="Takeaway 3",
        ),
    ]
