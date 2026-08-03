"""
Smoke test for the Summarizer component.

Run with:

  python scratch/digest/smoke_summarizer.py
"""

from health_ai_digest.digest import Summarizer
from health_ai_digest.llm import GroqClient
from health_ai_digest.models import (
  Article, 
  RankedArticle,
  SourceType,
)

def build_sample_article() -> RankedArticle:
  # Create a sample RankedArticle for manual testing.

  article = Article(
    title=(
      "Artificial Intelligence Improves Early Detection "
      "of Lung Cancer in Chest CT Scans"
    ),
    source=SourceType.PUBMED,
    url="https://pubmed.ncbi.nlm.nih.gov/12345678/",
    abstract=(
      "Researchers evaluated a deep learning model capable "
      "of identifying pulmonary nodules from chest CT images. "
      "The system achieved a sensitivity of 94% while reducing "
      "false positives compared with conventional CAD systems. "
      "The study included over 10,000 patients from multiple "
      "medical centers."
    ),
    journal="Journal of Medical AI",
    publication_date="2026-07-20",
    authors=[
      "John Smith",
      "Jane Doe",
    ],
    keywords=[
      "Artificial Intelligence",
      "Cancer Detection",
      "Deep Learning",
    ],
    doi="10.1000/example-doi",
  )

  return RankedArticle(
    article=article,
    score=97.5,
    relevance_score=0.95,
    recency_score=0.90,
    quality_score=0.92,
  )

def main() -> None:
  print("=" * 80)
  print("Summarizer Smoke Test")
  print("=" * 80)

  article = build_sample_article()

  summarizer = Summarizer(
    llm_client=GroqClient(),
  )

  summary = summarizer.summarize(article)

  print()
  print("TITLE")
  print("-" * 80)
  print(summary.ranked_article.article.title)

  print()
  print("SUMMARY")
  print("-" * 80)
  print(summary.summary)

  print()
  print("KEY TAKEAWAY")
  print("-" * 80)
  print(summary.key_takeaway)

  print("\nSCORES")
  print("-" * 80)
  print(f"Overall:   {summary.ranked_article.overall_score:.2f}")
  print(f"Relevance:   {summary.ranked_article.relevance_score:.2f}")
  print(f"Recency:   {summary.ranked_article.recency_score:.2f}")
  print(f"Quality:   {summary.ranked_article.quality_score:.2f}")

  print()
  print("=" * 80)
  print("Smoke test completed successfully.")
  print("=" * 80)

if __name__ == "__main__":
  main()
