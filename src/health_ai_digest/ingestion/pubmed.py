import requests
import xml.etree.ElementTree as ET

from health_ai_digest.ingestion.base import BaseIngestionClient
from health_ai_digest.models.article import Article
from health_ai_digest.models.enums import SourceType

class PubMedClient(BaseIngestionClient):
  SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
  FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

  def fetch(self, query: str, limit: int = 10) -> list[Article]:
    # Search PubMed and fetch full metadata for the resulting articles.
    pmids = self._search(query, limit)
    xml_data = self._fetch_details(pmids)
    articles = self._parse_articles(xml_data)

    return articles
  
  def _search(self, query: str, limit: int) -> list[str]:
    # Search PubMed and return a list of PMIDs.
    params = {
      "db": "pubmed",
      "term": query,
      "retmax": limit,
      "retmode": "json",
    }

    response = requests.get(self.SEARCH_URL, params=params)
    response.raise_for_status()

    data = response.json()

    return data["esearchresult"]["idlist"]
  
  def _fetch_details(self, pmids: list[str]) -> str:
    """
    Fetch article metadata from PubMed using PMIDs.
    Returns raw XML response.
    """
    if not pmids:
      return ""
    
    params = {
      "db": "pubmed",
      "id": ",".join(pmids),
      "retmode": "xml"
    }

    response = requests.get(self.FETCH_URL, params=params)
    response.raise_for_status()

    return response.text
  
  def _parse_articles(self, xml_data: str) -> list[Article]:
    if not xml_data:
      return []
    
    root = ET.fromstring(xml_data)
    articles = []

    for pubmed_article in root.findall(".//PubmedArticle"):
      article = self._parse_article(pubmed_article)
      articles.append(article)

    return articles
  
  def _parse_article(self, pubmed_article: ET.Element) -> Article:
    # Parse a single PubMed article.
    pmid = pubmed_article.findtext(".//PMID", default="")
    title = pubmed_article.findtext(".//ArticleTitle", default="Untitled")

    url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

    return Article(
      title=title,
      source=SourceType.PUBMED,
      url=url,
      abstract=None,
      published_at=None,
      keywords=[],
      doi=None,
    )