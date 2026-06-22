from abc import ABC, abstractmethod
from health_ai_digest.models.article import Article

class BaseIngestionClient(ABC):

  @abstractmethod
  def fetch(self, query: str) -> list[Article]:
    pass