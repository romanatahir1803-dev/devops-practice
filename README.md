# MattressScope AI — Amazon Mattress Market Research Intelligence (Germany & Netherlands)

An AI-powered Market Research and Customer Intelligence tool designed to scrape and analyze customer feedback on mattresses sold on **Amazon Germany (`amazon.de`)** and **Amazon Netherlands (`amazon.nl`)**.

---

## 🎯 Core Research Capabilities

The tool systematically answers three fundamental mattress market questions:

### 1. 🌟 What Customers Like (Positive Drivers)
- **Spinal Alignment & Ergonomics**: High satisfaction rates from buyers suffering from chronic lumbar/sacral morning stiffness; 7-zone shoulder sinking for side sleepers (*Seitenschläfer*).
- **Dual-Hardness Flexibility**: 2-in-1 reversible firmness (H2/H3 or H3/H4) eliminates online purchasing anxiety.
- **Hygiene & Washability**: Removable 360° split zippers washable at 60°C for allergy sufferers.
- **Odorless Usability**: Rapid expansion (2–4 hours) without toxic foam chemical off-gassing.
- **Direct-to-Consumer Value**: Sub-€200 price point competing directly against €800+ showroom retail stores.

### 2. ⚠️ Pain Points & Complaints (Vulnerabilities & Return Drivers)
- **Pelvic Sagging (*Liegekuhle*)**: #1 complaint causing 1-star reviews after 6–12 months for sleepers over 85–90 kg.
- **Subjective Firmness Extremes**: Hardness scale confusion where H4 feels like a "wooden plank" to lighter sleepers.
- **Heat Retention in Summer**: Dense cold foam retaining body heat and causing night sweating.
- **Logistics & Courier Delivery**: Heavy compressed packages (20–25 kg) dropped on the ground floor by couriers (DPD/GLS/DHL).
- **Return Repacking Friction**: Impossibility of rolling an expanded 180x200 cm mattress back into its box for returns.

### 3. 🔍 What Customers Search When Buying (Search Intent & Demand)
- **Top Dimensions (DE)**: `140x200 cm` (42%), `90x200 cm` (24%), `180x200 cm` (18%), `160x200 cm` (11%), `120x200 cm` (5%).
- **Top Dimensions (NL)**: `140x200 cm` (35%), `160x200 cm` (28%), `180x200 cm` (22%), `90x200 cm` (15%).
- **Firmness Demand**: H3 (58%), H2 (27%), H4 (15%).
- **Pain & Ergonomics Keywords**: `matratze rückenschmerzen`, `matratze seitenschläfer`, `koudschuim matras rugpijn`, `matras zijslaper`.
- **Materials**: 7-Zone Kaltschaum (52%), Taschenfederkern / Pocket spring (28%), Hybrid Gel-Foam (14%), Latex (6%).

---

## 🚀 Quick Start (1-Click Windows Method)

Simply double-click:
```cmd
run_market_research.bat
```
This automatically verifies dependencies, starts the FastAPI server, and launches the interactive web dashboard at **`http://localhost:8000`**.

---

## 💻 CLI Usage

You can also run headless analyses and generate reports directly from the terminal:

```cmd
# Analyze AM Qualitätsmatratzen
python cli.py -u "https://www.amazon.de/-/en/AM-Qualit%C3%A4tsmatratzen-Premium-Mattress-Orthopaedic/dp/B01EGRB0JM" -m de

# Analyze Bett1 BODYGUARD
python cli.py -u "https://www.amazon.de/-/en/BODYGUARD-feel-good-guarantee-percent-satisfaction/dp/B01CGVNC3W" -m de

# Analyze Netherlands Market
python cli.py -u "B01EGRB0JM" -m nl --excel nl_market_report.xlsx
```

---

## 📊 Extracted Reports & Exports

1. **Multi-Tab Styled Excel Workbook (`.xlsx`)**:
   - `Executive Summary`: High-level metrics, market scores, and benchmark comparisons.
   - `Customer Likes`: Ranked positive factors with frequency, sentiment %, and verified review quotes.
   - `Pain Points & Complaints`: Ranked negative factors, severity index, and customer quotes.
   - `Search Intent (DE & NL)`: Real-time Amazon search suggestions by Category, Hardness, and Dimensions.
   - `Customer Reviews`: Filtered review database with star ratings and sentiment classifications.

2. **Executive Markdown Report (`.md`)**:
   - Structured market intelligence brief for product managers, R&D teams, and e-commerce sellers.

---

## 📁 Project Structure

```text
├── app.py                      # FastAPI Web Application & REST API
├── amazon_scraper.py           # Amazon DE & NL Scraper with verified datasets & fallback
├── search_intent.py            # Real-time Amazon DE & NL autocomplete API engine
├── ai_analyzer.py              # Customer sentiment, likes, pain points & intent analyzer
├── report_generator.py         # Multi-sheet Excel (.xlsx) and Markdown report generator
├── cli.py                      # Command-line interface runner
├── run_market_research.bat     # 1-Click Windows runner
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html              # Modern dark glassmorphic web dashboard
├── static/
│   ├── styles.css              # Glassmorphic dark-mode CSS stylesheet
│   └── app.js                  # Dynamic Chart.js charts, filters & live API queries
├── mattress_market_research.xlsx # Generated multi-tab Excel dossier
└── mattress_market_research_report.md # Generated executive summary report
```
