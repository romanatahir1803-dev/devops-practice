"""
CLI Runner for Amazon Mattress Market Research Tool (DE & NL)
Allows command-line extraction, sentiment scoring, search intent discovery, and report generation.
"""

import argparse
import sys
import io

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from amazon_scraper import fetch_amazon_product_data
from search_intent import get_market_search_intent
from ai_analyzer import analyze_product_feedback
from report_generator import generate_excel_report, generate_markdown_report


def run_cli():
    parser = argparse.ArgumentParser(description="Amazon Mattress AI Market Research Tool")
    parser.add_argument(
        "--url", "-u",
        type=str,
        default="https://www.amazon.de/-/en/AM-Qualit%C3%A4tsmatratzen-Premium-Mattress-Orthopaedic/dp/B01EGRB0JM",
        help="Amazon product URL or ASIN (e.g. B01EGRB0JM or B01CGVNC3W)"
    )
    parser.add_argument(
        "--market", "-m",
        type=str,
        default="de",
        choices=["de", "nl"],
        help="Target Amazon marketplace: 'de' for Germany, 'nl' for Netherlands"
    )
    parser.add_argument(
        "--excel", "-x",
        type=str,
        default="mattress_market_research.xlsx",
        help="Output path for Excel report"
    )
    parser.add_argument(
        "--markdown", "-d",
        type=str,
        default="mattress_market_research_report.md",
        help="Output path for Markdown report"
    )

    args = parser.parse_args()

    print("=" * 70)
    print(" [MARKET RESEARCH] AMAZON MATTRESS AI TOOL (DE & NL)")
    print("=" * 70)
    print(f"Target Input: {args.url}")
    print(f"Target Market: {'[DE] Germany (Amazon.de)' if args.market == 'de' else '[NL] Netherlands (Amazon.nl)'}")
    print("\n[1/3] Extracting Product & Customer Review Data...")
    
    product = fetch_amazon_product_data(args.url, market=args.market)
    print(f" -> Found: {product.get('title')}")
    print(f" -> Brand: {product.get('brand')} | ASIN: {product.get('asin')}")
    print(f" -> Rating: {product.get('rating')} / 5.0 ({product.get('review_count'):,} reviews)")
    print(f" -> Loaded {len(product.get('reviews', []))} in-depth verified reviews.")

    print("\n[2/3] Mining Live Buyer Search Intent & Autocomplete Queries...")
    search_intent = get_market_search_intent(args.market)
    print(f" -> Discovered {search_intent.get('total_keywords')} high-intent search queries.")
    for cat, count in search_intent.get("categories", {}).items():
        print(f"    * {cat}: {count} queries")

    print("\n[3/3] Running AI Sentiment, Likes & Pain Points Analysis...")
    analysis = analyze_product_feedback(product, search_intent)

    print("\n" + "-" * 70)
    print(" [*] WHAT CUSTOMERS LIKE (TOP POSITIVE DRIVERS):")
    print("-" * 70)
    for like in analysis.get("what_they_like", [])[:3]:
        print(f" #{like['rank']} [{like['category']}] - {like['title']} ({like['share_pct']}% Positive)")
        print(f"    Evidence: \"{like['sample_feedback']}\"\n")

    print("-" * 70)
    print(" [!] CRITICAL PAIN POINTS & COMPLAINTS:")
    print("-" * 70)
    for pain in analysis.get("pain_points", [])[:3]:
        print(f" #{pain['rank']} [{pain['severity']}] - {pain['title']} ({pain['frequency_pct']}% Frequency)")
        print(f"    Evidence: \"{pain['sample_complaint']}\"\n")

    # Generate Reports
    excel_file = generate_excel_report(analysis, search_intent, args.excel)
    md_file = generate_markdown_report(analysis, search_intent, args.markdown)

    print("=" * 70)
    print(f"[OK] Multi-tab Excel Report saved to: {excel_file}")
    print(f"[OK] Executive Markdown Report saved to: {md_file}")
    print("=" * 70)


if __name__ == "__main__":
    run_cli()
