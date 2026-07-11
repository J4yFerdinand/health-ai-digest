import pytest

from health_ai_digest.digest.formatter import ArticleSummaryFormatter

@pytest.fixture
def formatter():
  # Return a formatter instance.
  return ArticleSummaryFormatter()

def test_parse_valid_response(formatter, ranked_article_factory):
  # A valid LLM response should produce an ArticleSummary.

  ranked_article = ranked_article_factory(
    title="Medical AI",
    score=0.91,
  )

  response = """
Summary:
Researchers developed an AI model that improves cancer detection accuracy.

Key Takeaway:
AI significantly improves diagnostic performance.
"""

  article_summary = formatter.parse(response, ranked_article)

  assert article_summary.ranked_article == ranked_article
  assert (
    article_summary.summary
    == "Researchers developed an AI model that improves cancer detection accuracy."
  )
  assert (
    article_summary.key_takeaway
    == "AI significantly improves diagnostic performance."
  )

def test_parse_preserves_ranked_article(formatter, ranked_article_factory):
  # The original RankedArticle should be preserved.
  ranked_article = ranked_article_factory()

  response = """
Summary:
Test summary.

Key Takeaway:
Test takeaway.
"""

  article_summary = formatter.parse(response, ranked_article)

  assert article_summary.ranked_article is ranked_article

def test_parse_trims_extra_whitespace(formatter, ranked_article_factory):
  # Extra whitespace should be removed
  ranked_article = ranked_article_factory()

  response = """
Summary:

Researchers created a useful AI model.

Key Takeaway:

Useful for clinical diagnosis.
"""

  article_summary = formatter.parse(response, ranked_article)

  assert article_summary.summary == "Researchers created a useful AI model."
  assert article_summary.key_takeaway == "Useful for clinical diagnosis."

def test_parse_rejects_empty_response(formatter, ranked_article_factory):
  # Empty responses should raise an error.
  ranked_article = ranked_article_factory()

  with pytest.raises(
    ValueError, 
    match="LLM response cannot be empty."
  ):
    formatter.parse("", ranked_article)

def test_parse_requires_summary_section(formatter, ranked_article_factory):
  # Responses must contain a "Summary:" section.
  ranked_article = ranked_article_factory()

  response = """
Key Takeaway:
AI improves diagnosis.
"""

  with pytest.raises(
    ValueError,
    match=r"Missing 'Summary:' section\.",
  ):
    formatter.parse(response, ranked_article)

def test_parse_requires_key_takeaway_section(
  formatter, 
  ranked_article_factory,
):
  # Responses must contain a "Key Takeaway:" section.
  ranked_article = ranked_article_factory()

  response = """
Summary:
Researchers developed an AI model.
"""

  with pytest.raises(
    ValueError,
    match=r"Missing 'Key Takeaway:' section\.",
  ):
    formatter.parse(response, ranked_article)

def test_parse_rejects_empty_summary(
  formatter,
  ranked_article_factory,
):
  # Summary cannot be empty.
  ranked_article = ranked_article_factory()

  response = """
Summary:

Key Takeaway:
Useful takeaway.
"""

  with pytest.raises(
    ValueError,
    match="Summary cannot be empty."
  ):
    formatter.parse(response, ranked_article)

def test_parse_rejects_empty_takeaway(
  formatter,
  ranked_article_factory,
):
  # Key takeaway cannot be empty.
  ranked_article = ranked_article_factory()

  response = """
Summary:
Researchers developed an AI model.

Key Takeaway:
"""

  with pytest.raises(
    ValueError,
    match="Key takeaway cannot be empty.",
  ):
    formatter.parse(response, ranked_article)