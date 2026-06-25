from health_ai_digest.aggregation.deduplicator import Deduplicator
from health_ai_digest.models.article import Article
from health_ai_digest.models.enums import SourceType

def create_article(
    title: str,
    url: str,
    doi: str | None = None,
) -> Article:
  return Article(
    title=title,
    source=SourceType.PUBMED,
    url=url,
    doi=doi,
  )

def test_returns_all_articles_by_url():
  deduplicator = Deduplicator()

  articles = [
    create_article("Paper 1", "https://paper1", "10.1"),
    create_article("Paper 2", "https://paper2", "10.2"),
    create_article("Paper 3", "https://paper3", "10.3"),
  ]

  result = deduplicator.deduplicate(articles)

  assert len(result) == 3

def test_deduplicates_articles_by_doi():
  deduplicator = Deduplicator()

  articles = [
    create_article("Paper 1", "https://paper1", "10.1000/abc"),
    create_article("Paper 1 duplicate", "https://paper2", "10.1000/abc"),
  ]

  result = deduplicator.deduplicate(articles)

  assert len(result) == 1
  assert result[0].doi == "10.1000/abc"

def test_deduplicates_articles_by_normalized_title():
  deduplicator = Deduplicator()

  articles = [
    create_article("AI Diagnosis Study", "https://paper1"),
    create_article("ai diagnosis study", "https://paper2"),
  ]

  result = deduplicator.deduplicate(articles)

  assert len(result) == 1
  assert result[0].title == "AI Diagnosis Study"