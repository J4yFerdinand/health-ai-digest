from health_ai_digest.models.article import Article
from health_ai_digest.models.enums import SourceType

def test_article_creation():
  article = Article(
    title="AI diagnosis paper",
    source=SourceType.PUBMED,
    url="https://example.com",
  )

  assert article.title == "AI diagnosis paper"
  assert article.source == SourceType.PUBMED