from enum import Enum

class SourceType(str, Enum):
  PUBMED = 'pubmed'
  ARXIV = 'arxiv'
  RSS = 'rss'