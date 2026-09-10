"""
Smoke Test
==========

Purpose:
  Validate the article summary formatter manually.

Run:

  python -m scratch.digest.smoke_formatter

Expected:

  Converts a valid LLM response into an ArticleSummary
  while preserving the original article data.
"""

from health_ai_digest.digest.formatter import ArticleSummaryFormatter
from health_ai_digest.models import (
    Article,
    ArticleSummary,
    RankedArticle,
    SourceType,
)
from scratch.common import build_article, print_header, print_section, print_success


def main() -> None:
    print_header("Article Summary Formatter")

    article = build_article("AI for Cardiology", 5)

    ranked_article = RankedArticle(
        article=article,
        overall_score=0.90,
        relevance_score=0.95,
        recency_score=0.85,
        quality_score=0.90,
    )

    expected_summary = (
        "This study evaluates the use of artificial intelligence\n"
        "for improving diagnostic support in cardiology."
    )

    expected_key_takeaway = (
        "AI-assisted tools may improve diagnostic accuracy\n"
        "when combined with clinician expertise."
    )

    response = (
        "Summary:\n"
        f"{expected_summary}\n\n"
        "Key Takeaway:\n"
        f"{expected_key_takeaway}"
    )

    formatter = ArticleSummaryFormatter()

    result = formatter.parse(
        response,
        ranked_article,
    )

    # --------------------------------------------------------
    # * Basic Formatting
    # --------------------------------------------------------

    print_section("Basic Formatting")

    result_type = type(result).__name__
    summary_valid = bool(result.summary.strip())
    key_takeaway_valid = bool(result.key_takeaway.strip())
    ranked_article_preserved = result.ranked_article is ranked_article

    print(f"Result Type              : {result_type}")
    print(f"Summary Generated        : {summary_valid}")
    print(f"Key Takeaway Generated   : {key_takeaway_valid}")
    print(f"Ranked Article Preserved : {ranked_article_preserved}")

    assert isinstance(result, ArticleSummary)
    assert summary_valid
    assert key_takeaway_valid
    assert ranked_article_preserved

    # --------------------------------------------------------
    # * Data Preservation
    # --------------------------------------------------------
    print_section("\nData Preservation")

    summary_preserved = result.summary == expected_summary
    key_takeaway_preserved = result.key_takeaway == expected_key_takeaway

    article_title_preserved = result.ranked_article.article.title == article.title

    article_source_preserved = result.ranked_article.article.source == article.source

    article_url_preserved = result.ranked_article.article.url == article.url

    article_abstract_preserved = (
        result.ranked_article.article.abstract == article.abstract
    )

    article_authors_preserved = result.ranked_article.article.authors == article.authors

    article_published_preserved = (
        result.ranked_article.article.published_at == article.published_at
    )

    article_keywords_preserved = (
        result.ranked_article.article.keywords == article.keywords
    )

    article_doi_preserved = result.ranked_article.article.doi == article.doi

    print(f"Summary Preserved          : {summary_preserved}")
    print(f"Key Takeaway Preserved     : {key_takeaway_preserved}")
    print(f"Article Title Preserved    : {article_title_preserved}")
    print(f"Article Source Preserved   : {article_source_preserved}")
    print(f"Article URL Preserved      : {article_url_preserved}")
    print(f"Article Abstract Preserved : {article_abstract_preserved}")
    print(f"Article Authors Preserved  : {article_authors_preserved}")
    print(f"Published Date Preserved   : " f"{article_published_preserved}")
    print(f"Article Keywords Preserved : {article_keywords_preserved}")
    print(f"Article DOI Preserved      : {article_doi_preserved}")

    assert summary_preserved
    assert key_takeaway_preserved
    assert article_title_preserved
    assert article_source_preserved
    assert article_url_preserved
    assert article_abstract_preserved
    assert article_authors_preserved
    assert article_published_preserved
    assert article_keywords_preserved
    assert article_doi_preserved

    optional_article = Article(
        title="Optional Data Article",
        source=SourceType.PUBMED,
        url="https://example.com/optional-data",
    )

    optional_ranked_article = RankedArticle(
        article=optional_article,
        overall_score=0.75,
        relevance_score=0.80,
        recency_score=0.70,
        quality_score=0.75,
    )

    optional_summary = "This article contains only the required article data."

    optional_key_takeaway = (
        "The formatter should still process the response successfully."
    )

    optional_response = (
        "Summary:\n"
        f"{optional_summary}\n\n"
        "Key Takeaway:\n"
        f"{optional_key_takeaway}"
    )

    optional_result = formatter.parse(
        optional_response,
        optional_ranked_article,
    )

    # --------------------------------------------------------
    # * Optional Data
    # --------------------------------------------------------

    print_section("\nOptional Data")

    optional_result_valid = isinstance(
        optional_result,
        ArticleSummary,
    )

    optional_summary_valid = optional_result.summary == optional_summary

    optional_key_takeaway_valid = optional_result.key_takeaway == optional_key_takeaway

    optional_ranked_article_preserved = (
        optional_result.ranked_article is optional_ranked_article
    )

    optional_abstract_empty = optional_result.ranked_article.article.abstract is None

    optional_authors_empty = not (optional_result.ranked_article.article.authors)

    optional_published_empty = (
        optional_result.ranked_article.article.published_at is None
    )

    optional_keywords_empty = optional_result.ranked_article.article.keywords == []

    optional_doi_empty = optional_result.ranked_article.article.doi is None

    print(f"Result Type Valid            : {optional_result_valid}")
    print(f"Summary Preserved            : {optional_summary_valid}")
    print(f"Key Takeaway Preserved       : " f"{optional_key_takeaway_valid}")
    print(f"Ranked Article Preserved     : " f"{optional_ranked_article_preserved}")
    print(f"Abstract Remains Empty       : " f"{optional_abstract_empty}")
    print(f"Authors Remain Empty         : " f"{optional_authors_empty}")
    print(f"Published Date Remains Empty : " f"{optional_published_empty}")
    print(f"Keywords Remain Empty        : " f"{optional_keywords_empty}")
    print(f"DOI Remains Empty            : " f"{optional_doi_empty}")

    assert optional_result_valid
    assert optional_summary_valid
    assert optional_key_takeaway_valid
    assert optional_ranked_article_preserved
    assert optional_abstract_empty
    assert optional_authors_empty
    assert optional_published_empty
    assert optional_keywords_empty
    assert optional_doi_empty

    # --------------------------------------------------------
    # * Malformed Response
    # --------------------------------------------------------
    print_section("\nMalformed Response")

    missing_summary_response = (
        "Key Takeaway:\n" "AI-assisted tools may improve diagnostic accuracy."
    )

    try:
        formatter.parse(
            missing_summary_response,
            ranked_article,
        )
        missing_summary_rejected = False
    except ValueError:
        missing_summary_rejected = True

    print(f"Missing Summary      : " f"{missing_summary_rejected}")

    assert missing_summary_rejected

    missing_key_takeaway_response = (
        "Summary:\n" "This study evaluates the use of artificial intelligence."
    )

    try:
        formatter.parse(
            missing_key_takeaway_response,
            ranked_article,
        )
        missing_key_takeaway_rejected = False
    except ValueError:
        missing_key_takeaway_rejected = True

    print(f"Missing Key Takeaway : " f"{missing_key_takeaway_rejected}")

    assert missing_key_takeaway_rejected

    empty_summary_response = (
        "Summary:\n"
        "\n"
        "Key Takeaway:\n"
        "AI-assisted tools may improve diagnostic accuracy."
    )

    try:
        formatter.parse(
            empty_summary_response,
            ranked_article,
        )
        empty_summary_rejected = False
    except ValueError:
        empty_summary_rejected = True

    print(f"Empty Summary        : " f"{empty_summary_rejected}")

    assert empty_summary_rejected

    empty_key_takeaway_response = (
        "Summary:\n"
        "This study evaluates the use of artificial intelligence."
        "\n\n"
        "Key Takeaway:\n"
    )

    try:
        formatter.parse(
            empty_key_takeaway_response,
            ranked_article,
        )
        empty_key_takeaway_rejected = False
    except ValueError:
        empty_key_takeaway_rejected = True

    print(f"Empty Key Takeaway   : " f"{empty_key_takeaway_rejected}")

    assert empty_key_takeaway_rejected

    empty_response = ""

    try:
        formatter.parse(
            empty_response,
            ranked_article,
        )
        empty_response_rejected = False
    except ValueError:
        empty_response_rejected = True

    print(f"Empty Response       : " f"{empty_response_rejected}")

    assert empty_response_rejected

    # --------------------------------------------------------
    # * Whitespace Handling
    # --------------------------------------------------------

    print_section("\nWhitespace Handling")

    whitespace_summary = "This study evaluates the use of artificial intelligence."

    whitespace_key_takeaway = "AI-assisted tools may improve diagnostic accuracy."

    whitespace_response = (
        "Summary:\n"
        "\n"
        f"   {whitespace_summary}   \n"
        "Key Takeaway:\n"
        "\n"
        f"   {whitespace_key_takeaway}   \n"
    )

    whitespace_result = formatter.parse(
        whitespace_response,
        ranked_article,
    )

    whitespace_summary_clean = whitespace_result.summary == whitespace_summary

    whitespace_key_takeaway_clean = (
        whitespace_result.key_takeaway == whitespace_key_takeaway
    )

    print(f"Summary Whitespace Removed      : " f"{whitespace_summary_clean}")
    print(f"Key Takeaway Whitespace Removed : " f"{whitespace_key_takeaway_clean}")

    assert whitespace_summary_clean
    assert whitespace_key_takeaway_clean

    # --------------------------------------------------------
    # * Multiline Content
    # --------------------------------------------------------
    print_section("\nMultiline Content")

    multiline_summary = (
        "This study evaluates the use of artificial intelligence\n"
        "for improving diagnostic support in cardiology.\n"
        "The approach combines automated analysis with.\n"
        "clinical expertise."
    )

    multiline_key_takeaway = (
        "AI-assisted tools may improve diagnostic accuracy\n"
        "when combined with clinician expertise."
    )

    multiline_response = (
        "Summary:\n"
        f"{multiline_summary}\n\n"
        "Key Takeaway:\n"
        f"{multiline_key_takeaway}"
    )

    multiline_result = formatter.parse(
        multiline_response,
        ranked_article,
    )

    multiline_summary_preserved = multiline_result.summary == multiline_summary

    multiline_key_takeaway_preserved = (
        multiline_result.key_takeaway == multiline_key_takeaway
    )

    print(f"Summary Line Breaks Preserved      : " f"{multiline_summary_preserved}")
    print(
        f"Key Takeaway Line Breaks Preserved : " f"{multiline_key_takeaway_preserved}"
    )

    assert multiline_summary_preserved
    assert multiline_key_takeaway_preserved

    # --------------------------------------------------------
    # * Section Separator Handling
    # -------------------------------------------------------
    print_section("\nSection Separator Handling")

    separator_summary = (
        "This study discusses the concept of " "Key Takeaway: within its analysis."
    )

    separator_key_takeaway = (
        "The results may support improved clinical decision-making."
    )

    separator_response = (
        "Summary:\n"
        f"{separator_summary}\n\n"
        "Key Takeaway:\n"
        f"{separator_key_takeaway}"
    )

    separator_result = formatter.parse(
        separator_response,
        ranked_article,
    )

    separator_summary_preserved = separator_result.summary == separator_summary

    separator_key_takeaway_preserved = (
        separator_result.key_takeaway == separator_key_takeaway
    )

    print(f"Summary Internal Marker Preserved      : " f"{separator_summary_preserved}")
    print(
        f"Key Takeaway Correctly Extracted       : "
        f"{separator_key_takeaway_preserved}"
    )

    assert separator_summary_preserved
    assert separator_key_takeaway_preserved

    # --------------------------------------------------------
    # * Summary Marker Handling
    # --------------------------------------------------------
    print_section("\nSummary Marker Handling")

    marker_summary = "The study defines Summary: as a useful reporting concept."

    marker_key_takeaway = "Clear summaries can improve clinical communication."

    marker_response = (
        "Summary:\n" f"{marker_summary}\n\n" "Key Takeaway:\n" f"{marker_key_takeaway}"
    )

    marker_result = formatter.parse(
        marker_response,
        ranked_article,
    )

    marker_summary_preserved = marker_result.summary == marker_summary

    marker_key_takeaway_preserved = marker_result.key_takeaway == marker_key_takeaway

    print(f"Summary Internal Marker Preserved      : " f"{marker_summary_preserved}")
    print(
        f"Key Takeaway Correctly Extracted       : " f"{marker_key_takeaway_preserved}"
    )

    assert marker_summary_preserved
    assert marker_key_takeaway_preserved

    # --------------------------------------------------------
    # * Separator Whitespace Handling
    # --------------------------------------------------------
    print_section("\nSeparator Whitespace Handling")

    separator_whitespace_summary = (
        "This study evaluates artificial intelligence " "for clinical decision support."
    )

    separator_whitespace_key_takeaway = (
        "AI-assisted tools may support clinical decision-making."
    )

    separator_whitespace_response = (
        "Summary:\n"
        f"   {separator_whitespace_summary}   \n"
        "Key Takeaway:\n"
        f"   {separator_whitespace_key_takeaway}   \n"
    )

    separator_key_takeaway_whitespace_result = formatter.parse(
        separator_whitespace_response,
        ranked_article,
    )

    separator_whitespace_summary_preserved = (
        separator_key_takeaway_whitespace_result.summary == separator_whitespace_summary
    )

    separator_whitespace_key_takeaway_preserved = (
        separator_key_takeaway_whitespace_result.key_takeaway
        == separator_whitespace_key_takeaway
    )

    print(
        f"Summary Preserved                 : "
        f"{separator_whitespace_summary_preserved}"
    )
    print(
        f"Key Takeaway Preserved            : "
        f"{separator_whitespace_key_takeaway_preserved}"
    )

    assert separator_whitespace_summary_preserved
    assert separator_whitespace_key_takeaway_preserved

    # --------------------------------------------------------
    # * Case Handling
    # --------------------------------------------------------
    print_section("\nCase Handling")

    case_summary = (
        "This study evaluates artificial intelligence " "for clinical decision support."
    )

    case_key_takeaway = "AI-assisted tools may support clinical decision-making."

    case_variations = [
        (
            "Uppercase",
            "SUMMARY:",
            "KEY TAKEAWAY:",
        ),
        (
            "Lowercase",
            "summary:",
            "key takeaway:",
        ),
        (
            "Mixed Case",
            "SuMmArY:",
            "KeY TaKeAwAy:",
        ),
    ]

    for case_name, summary_marker, key_takeaway_marker in case_variations:
        case_response = (
            f"{summary_marker}\n"
            f"{case_summary}\n\n"
            f"{key_takeaway_marker}\n"
            f"{case_key_takeaway}"
        )

        try:
            case_result = formatter.parse(
                case_response,
                ranked_article,
            )

            case_summary_preserved = case_result.summary == case_summary

            case_key_takeaway_preserved = case_result.key_takeaway == case_key_takeaway

        except ValueError:
            case_summary_preserved = False
            case_key_takeaway_preserved = False

        print(f"{case_name} Summary Preserved        : " f"{case_summary_preserved}")
        print(
            f"{case_name} Key Takeaway Preserved    : " f"{case_key_takeaway_preserved}"
        )

        assert case_summary_preserved
        assert case_key_takeaway_preserved

    print_success()


if __name__ == "__main__":
    main()
