from abc import ABC, abstractmethod
from health_ai_digest.models.article import Article

class BaseIngestionClient(ABC):

  @abstractmethod
  def fetch(self, query: str, limit: int = 10) -> list[Article]:
    """
    Fetch articles from a source based on a search query.
    """
    pass