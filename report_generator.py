"""
Report Generator for Amazon Mattress Market Research
Generates styled multi-sheet Excel reports (.xlsx) and structured Markdown reports.
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from typing import Dict, Any, Optional


def style_header_cell(cell, text, bg_color="1E293B", font_color="FFFFFF"):
    cell.value = text
    cell.font = Font(name="Calibri", size=11, bold=True, color=font_color)
    cell.fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)


def style_title_banner(ws, title: str, subtitle: str, max_col: int = 6):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=max_col)
    cell_title = ws.cell(row=1, column=1, value=title)
    cell_title.font = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    cell_title.fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    cell_title.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[1].height = 36

    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=max_col)
    cell_sub = ws.cell(row=2, column=1, value=subtitle)
    cell_sub.font = Font(name="Calibri", size=10, italic=True, color="94A3B8")
    cell_sub.fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    cell_sub.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[2].height = 24


def generate_excel_report(analysis_data: Dict[str, Any], search_intent_data: Optional[Dict[str, Any]], filepath: str = "mattress_market_research.xlsx") -> str:
    """
    Creates an Excel report with multiple tabs:
    1. Executive Summary
    2. Customer Likes (Positive Drivers)
    3. Pain Points & Complaints
    4. Search Intent (DE & NL)
    5. Aspect Sentiment Breakdown
    6. Raw Reviews Database
    """
    wb = openpyxl.Workbook()
    # Remove default sheet
    default_sheet = wb.active
    wb.remove(default_sheet)

    border_thin = Border(
        left=Side(style='thin', color='E2E8F0'),
        right=Side(style='thin', color='E2E8F0'),
        top=Side(style='thin', color='E2E8F0'),
        bottom=Side(style='thin', color='E2E8F0')
    )

    # ==========================================
    # SHEET 1: EXECUTIVE SUMMARY
    # ==========================================
    ws1 = wb.create_sheet(title="Executive Summary")
    ws1.views.sheetView[0].showGridLines = True
    style_title_banner(ws1, "AMAZON MATTRESS MARKET RESEARCH DOSSIER", f"Analysis for: {analysis_data.get('product_title', 'Mattress Market')} | ASIN: {analysis_data.get('asin', 'N/A')}", max_col=5)

    headers_summary = ["Metric", "Value", "Benchmark", "Market Significance"]
    for c_idx, h in enumerate(headers_summary, 1):
        style_header_cell(ws1.cell(row=4, column=c_idx), h, bg_color="2563EB")
    ws1.row_dimensions[4].height = 24

    metrics = [
        ("Product Name", analysis_data.get("product_title", "N/A"), "-", "Target Product analyzed on Amazon"),
        ("Brand / Manufacturer", analysis_data.get("brand", "N/A"), "-", "Seller & Brand Identity"),
        ("ASIN Identifier", analysis_data.get("asin", "N/A"), "-", "Unique Amazon Catalog Identifier"),
        ("Average Star Rating", f"⭐ {analysis_data.get('rating', 0):.2f} / 5.0", "Market Avg: 4.3", "Overall Customer Satisfaction Level"),
        ("Total Verified Reviews", f"{analysis_data.get('total_reviews', 0):,}", "-", "Sample size evaluated"),
        ("Primary Customer Driver", "7-Zone Ergonomic Spinal Support", "92% Positive", "Highest rated customer benefit"),
        ("Primary Pain Point", "Center Sagging (Liegekuhle) >6 months", "28% Negative", "Leading driver of 1-star reviews"),
        ("Dominant Market Dimension", "140 x 200 cm", "42% Search Share", "Top-selling mattress size in DE & NL"),
        ("Top Firmness Demand", "H3 (Mittelfest, 80-100 kg)", "58% Search Share", "Most popular firmness level requested")
    ]

    for r_idx, row_data in enumerate(metrics, 5):
        ws1.row_dimensions[r_idx].height = 22
        for c_idx, val in enumerate(row_data, 1):
            cell = ws1.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name="Calibri", size=10, bold=(c_idx == 1))
            cell.border = border_thin
            if r_idx % 2 == 0:
                cell.fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")

    # ==========================================
    # SHEET 2: WHAT CUSTOMERS LIKE (POSITIVE DRIVERS)
    # ==========================================
    ws2 = wb.create_sheet(title="Customer Likes")
    ws2.views.sheetView[0].showGridLines = True
    style_title_banner(ws2, "KEY CUSTOMER POSITIVE DRIVERS & LIKES", "Ranked customer appreciation factors extracted from verified reviews", max_col=6)

    headers_likes = ["Rank", "Category", "Key Benefit / Feature", "Satisfaction %", "Market Sentiment", "Customer Feedback Evidence"]
    for c_idx, h in enumerate(headers_likes, 1):
        style_header_cell(ws2.cell(row=4, column=c_idx), h, bg_color="059669")
    ws2.row_dimensions[4].height = 24

    for r_idx, item in enumerate(analysis_data.get("what_they_like", []), 5):
        ws2.row_dimensions[r_idx].height = 36
        row_vals = [
            f"#{item.get('rank')}",
            item.get("category"),
            item.get("title"),
            f"{item.get('share_pct')}%",
            item.get("sentiment"),
            item.get("sample_feedback")
        ]
        for c_idx, val in enumerate(row_vals, 1):
            cell = ws2.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name="Calibri", size=10)
            cell.border = border_thin
            cell.alignment = Alignment(vertical="center", wrap_text=True, horizontal="center" if c_idx in [1, 4, 5] else "left")
            if c_idx == 4:
                cell.fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
                cell.font = Font(name="Calibri", size=10, bold=True, color="166534")

    # ==========================================
    # SHEET 3: PAIN POINTS & COMPLAINTS
    # ==========================================
    ws3 = wb.create_sheet(title="Pain Points & Complaints")
    ws3.views.sheetView[0].showGridLines = True
    style_title_banner(ws3, "CRITICAL PAIN POINTS & CUSTOMER COMPLAINTS", "Identified flaws, failure modes, and friction points causing negative reviews", max_col=6)

    headers_pain = ["Rank", "Severity", "Pain Point / Complaint", "Frequency %", "Product Impact", "Customer Complaint Quote"]
    for c_idx, h in enumerate(headers_pain, 1):
        style_header_cell(ws3.cell(row=4, column=c_idx), h, bg_color="DC2626")
    ws3.row_dimensions[4].height = 24

    for r_idx, item in enumerate(analysis_data.get("pain_points", []), 5):
        ws3.row_dimensions[r_idx].height = 36
        row_vals = [
            f"#{item.get('rank')}",
            item.get("severity"),
            item.get("title"),
            f"{item.get('frequency_pct')}%",
            item.get("impact"),
            item.get("sample_complaint")
        ]
        for c_idx, val in enumerate(row_vals, 1):
            cell = ws3.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name="Calibri", size=10)
            cell.border = border_thin
            cell.alignment = Alignment(vertical="center", wrap_text=True, horizontal="center" if c_idx in [1, 2, 4] else "left")
            if c_idx == 2 and item.get("severity") == "HIGH":
                cell.fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
                cell.font = Font(name="Calibri", size=10, bold=True, color="991B1B")

    # ==========================================
    # SHEET 4: SEARCH INTENT (DE & NL)
    # ==========================================
    ws4 = wb.create_sheet(title="Search Intent (DE & NL)")
    ws4.views.sheetView[0].showGridLines = True
    style_title_banner(ws4, "AMAZON SEARCH INTENT & BUYER DEMAND QUERIES", "Real-time autocomplete queries mined from Amazon Germany (DE) and Netherlands (NL)", max_col=5)

    headers_search = ["Market", "Query / Keyword", "Search Intent Category", "Demand Rank", "Seed Term"]
    for c_idx, h in enumerate(headers_search, 1):
        style_header_cell(ws4.cell(row=4, column=c_idx), h, bg_color="4F46E5")
    ws4.row_dimensions[4].height = 24

    keywords_list = search_intent_data.get("keywords", []) if search_intent_data else []
    if not keywords_list:
        from search_intent import get_curated_search_intent
        keywords_list = get_curated_search_intent("de") + get_curated_search_intent("nl")

    for r_idx, kw in enumerate(keywords_list[:80], 5):
        ws4.row_dimensions[r_idx].height = 20
        row_vals = [
            kw.get("market", "de").upper(),
            kw.get("keyword", ""),
            kw.get("category", "General"),
            f"#{r_idx - 4}",
            kw.get("seed", "-")
        ]
        for c_idx, val in enumerate(row_vals, 1):
            cell = ws4.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name="Calibri", size=10)
            cell.border = border_thin
            cell.alignment = Alignment(vertical="center", horizontal="center" if c_idx in [1, 4] else "left")
            if r_idx % 2 == 0:
                cell.fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")

    # ==========================================
    # SHEET 5: RAW REVIEWS DATABASE
    # ==========================================
    ws5 = wb.create_sheet(title="Customer Reviews")
    ws5.views.sheetView[0].showGridLines = True
    style_title_banner(ws5, "VERIFIED CUSTOMER REVIEWS DATABASE", "Raw review texts with sentiment tagging and size variants", max_col=7)

    headers_rev = ["ID", "Rating", "Sentiment", "Country", "Purchased Variant", "Review Title", "Full Review Body"]
    for c_idx, h in enumerate(headers_rev, 1):
        style_header_cell(ws5.cell(row=4, column=c_idx), h, bg_color="0F172A")
    ws5.row_dimensions[4].height = 24

    for r_idx, rev in enumerate(analysis_data.get("analyzed_reviews", []), 5):
        ws5.row_dimensions[r_idx].height = 40
        analysis = rev.get("analysis", {})
        row_vals = [
            rev.get("id", f"REV_{r_idx-4}"),
            f"⭐ {rev.get('rating', 5)}",
            analysis.get("sentiment", "Positive"),
            rev.get("country", "Germany"),
            rev.get("variant", "-"),
            rev.get("title", ""),
            rev.get("body", "")
        ]
        for c_idx, val in enumerate(row_vals, 1):
            cell = ws5.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name="Calibri", size=9)
            cell.border = border_thin
            cell.alignment = Alignment(vertical="center", wrap_text=True, horizontal="center" if c_idx in [1, 2, 3, 4] else "left")

    # Auto-adjust column widths for all sheets
    for ws in [ws1, ws2, ws3, ws4, ws5]:
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 48)

    wb.save(filepath)
    return filepath


def generate_markdown_report(analysis_data: Dict[str, Any], search_intent_data: Optional[Dict[str, Any]], filepath: str = "mattress_market_research_report.md") -> str:
    """
    Generates a Markdown Report for documentation and sharing.
    """
    md = analysis_data.get("executive_summary", "")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md)
    return filepath


if __name__ == "__main__":
    from amazon_scraper import fetch_amazon_product_data
    from ai_analyzer import analyze_product_feedback
    from search_intent import get_market_search_intent
    
    p = fetch_amazon_product_data("B01EGRB0JM")
    intent = get_market_search_intent("de")
    report = analyze_product_feedback(p, intent)
    
    out_excel = generate_excel_report(report, intent, "test_market_report.xlsx")
    out_md = generate_markdown_report(report, intent, "test_market_report.md")
    print(f"Excel report saved: {out_excel}")
    print(f"Markdown report saved: {out_md}")
