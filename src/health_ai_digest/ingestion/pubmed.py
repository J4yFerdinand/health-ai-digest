import requests
import xml.etree.ElementTree as ET

from datetime import datetime

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

    authors = self._extract_authors(pubmed_article)
    published_at = self._extract_published_at(pubmed_article)

    return Article(
      title=title,
      source=SourceType.PUBMED,
      url=url,
      authors=authors,
      published_at=published_at,
    )

  def _extract_authors(self, pubmed_article: ET.Element) -> list[str]:
    # Extract author names from PubMed article XML
    authors = []

    for author in pubmed_article.findall(".//Author"):
      fore_name = author.findtext("ForeName")
      last_name = author.findtext("LastName")

      if fore_name and last_name:
        authors.append(f"{fore_name} {last_name}")
      elif last_name:
        authors.append(last_name)

    return authors

  def _extract_published_at(
    self,
    pubmed_article: ET.Element,
  ) -> datetime | None:
    # Extract publication date from PubMed article XML.
    pub_date = pubmed_article.find(".//PubDate")

    if pub_date is None:
      return None

    year = pub_date.findtext("Year")
    month = pub_date.findtext("Month", "1")
    day = pub_date.findtext("Day", "1")

    if not year:
      return None

    month_map = {
      "Jan": 1,
      "Feb": 2,
      "Mar": 3,
      "Apr": 4,
      "May": 5,
      "Jun": 6,
      "Jul": 7,
      "Aug": 8,
      "Sep": 9,
      "Oct": 10,
      "Nov": 11,
      "Dec": 12,
    }

    if month.isdigit():
      month_value = int(month)
    else:
      month_value = month_map.get(month, 1)

    try:
      return datetime(int(year), month_value, int(day))
    except ValueError:
      return None