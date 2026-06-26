import pytest

from health_ai_digest.models.article import Article
from health_ai_digest.models.enums import SourceType

@pytest.fixture
def article_factory():
  def _create_article(
      title: str = "Default Paper",
      url: str = "https://default-paper",
      doi: str | None = None,
  ) -> Article:
    return Article(
      title=title,
      source=SourceType.PUBMED,
      url=url,
      doi=doi,
    )
  
  return _create_article