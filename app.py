"""
FastAPI Server for Amazon Mattress Market Research AI Tool
Provides interactive web dashboard and REST API for market intelligence analysis.
"""

import os
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, Any

from amazon_scraper import fetch_amazon_product_data, extract_asin
from search_intent import get_market_search_intent
from ai_analyzer import analyze_product_feedback
from report_generator import generate_excel_report, generate_markdown_report

app = FastAPI(title="Amazon Mattress Market Research AI Tool")

# Create templates and static directories if they don't exist
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Cached storage for latest analysis
CURRENT_DATA: Dict[str, Any] = {
    "product": None,
    "analysis": None,
    "search_intent": None,
    "excel_path": "mattress_market_research.xlsx",
    "md_path": "mattress_market_research_report.md"
}


def ensure_data_loaded(asin: str = "B01EGRB0JM", market: str = "de"):
    if not CURRENT_DATA["analysis"] or CURRENT_DATA.get("current_asin") != asin:
        p = fetch_amazon_product_data(asin, market=market)
        intent = get_market_search_intent(market)
        analysis = analyze_product_feedback(p, intent)
        CURRENT_DATA["product"] = p
        CURRENT_DATA["analysis"] = analysis
        CURRENT_DATA["search_intent"] = intent
        CURRENT_DATA["current_asin"] = asin
        try:
            generate_excel_report(analysis, intent, CURRENT_DATA["excel_path"])
            generate_markdown_report(analysis, intent, CURRENT_DATA["md_path"])
        except Exception as e:
            print(f"Report generation note: {e}")


class AnalysisRequest(BaseModel):
    url_or_asin: str
    market: Optional[str] = "de"


@app.get("/")
def index():
    index_file = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    return FileResponse(index_file)


@app.get("/api/current")
def get_current_data():
    ensure_data_loaded("B01EGRB0JM", "de")
    return {
        "product": CURRENT_DATA["product"],
        "analysis": CURRENT_DATA["analysis"],
        "search_intent": CURRENT_DATA["search_intent"]
    }


@app.post("/api/analyze")
def analyze_endpoint(req: AnalysisRequest):
    url_or_asin = req.url_or_asin.strip()
    market = req.market or "de"
    
    p = fetch_amazon_product_data(url_or_asin, market=market)
    intent = get_market_search_intent(market)
    analysis = analyze_product_feedback(p, intent)
    
    CURRENT_DATA["product"] = p
    CURRENT_DATA["analysis"] = analysis
    CURRENT_DATA["search_intent"] = intent
    CURRENT_DATA["current_asin"] = p.get("asin")
    
    try:
        generate_excel_report(analysis, intent, CURRENT_DATA["excel_path"])
        generate_markdown_report(analysis, intent, CURRENT_DATA["md_path"])
    except Exception as e:
        print(f"Report generation note: {e}")
    
    return {
        "product": p,
        "analysis": analysis,
        "search_intent": intent
    }


@app.get("/api/comparison")
def get_comparison_data():
    am_data = fetch_amazon_product_data("B01EGRB0JM", market="de")
    intent_de = get_market_search_intent("de")
    am_analysis = analyze_product_feedback(am_data, intent_de)

    bett1_data = fetch_amazon_product_data("B01CGVNC3W", market="de")
    bett1_analysis = analyze_product_feedback(bett1_data, intent_de)

    return {
        "product_am": {
            "product": am_data,
            "analysis": am_analysis
        },
        "product_bett1": {
            "product": bett1_data,
            "analysis": bett1_analysis
        },
        "search_intent": intent_de
    }


@app.get("/api/export/excel")
def export_excel():
    ensure_data_loaded("B01EGRB0JM", "de")
    path = CURRENT_DATA.get("excel_path", "mattress_market_research.xlsx")
    return FileResponse(
        path=path,
        filename="Amazon_Mattress_Market_Research.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@app.get("/api/export/markdown")
def export_markdown():
    ensure_data_loaded("B01EGRB0JM", "de")
    path = CURRENT_DATA.get("md_path", "mattress_market_research_report.md")
    return FileResponse(
        path=path,
        filename="Amazon_Mattress_Market_Research.md",
        media_type="text/markdown"
    )


if __name__ == "__main__":
    import uvicorn
    print("Starting Amazon Mattress Market Research AI Dashboard on http://localhost:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
