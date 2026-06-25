from health_ai_digest.aggregation.deduplicator import Deduplicator

def test_returns_all_articles_when_no_duplicates(article_factory):
  deduplicator = Deduplicator()

  articles = [
    article_factory("Paper 1", "https://paper1", "10.1"),
    article_factory("Paper 2", "https://paper2", "10.2"),
    article_factory("Paper 3", "https://paper3", "10.3"),
  ]

  result = deduplicator.deduplicate(articles)

  assert len(result) == 3


def test_deduplicates_articles_by_doi(article_factory):
  deduplicator = Deduplicator()

  articles = [
    article_factory("Paper 1", "https://paper1", "10.1000/abc"),
    article_factory("Paper 1 duplicate", "https://paper2", "10.1000/abc"),
  ]

  result = deduplicator.deduplicate(articles)

  assert len(result) == 1
  assert result[0].doi == "10.1000/abc"


def test_deduplicates_articles_by_url(article_factory):
  deduplicator = Deduplicator()

  articles = [
    article_factory("Paper 1", "https://same-url"),
    article_factory("Paper 1 copy", "https://same-url"),
  ]

  result = deduplicator.deduplicate(articles)

  assert len(result) == 1
  assert result[0].url == "https://same-url"


def test_deduplicates_articles_by_normalized_title(article_factory):
  deduplicator = Deduplicator()

  articles = [
    article_factory("AI Diagnosis Study", "https://paper1"),
    article_factory(" ai diagnosis study ", "https://paper2"),
  ]

  result = deduplicator.deduplicate(articles)

  assert len(result) == 1
  assert result[0].title == "AI Diagnosis Study"