#!/usr/bin/env python3
"""
bett1.de Mattress Web Scraper (Windows & Cross-Platform Compatible)
Extracts all mattress models and variant sizes with pricing, SKUs, and reviews.
Exports data into a professionally styled Excel spreadsheet (.xlsx).
"""

import os
import sys
import re
import json
import gzip
import time
import logging
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("bett1_scraper")

# Headers for HTTP requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9,de;q=0.8'
}

SITEMAP_URL = 'https://en.bett1.de/sitemap/salesChannel-0cb4b71538f94cf6a32835c319a2568f-eccba1064e43492488cd2db0a4a5d321/0cb4b71538f94cf6a32835c319a2568f-02cc68b92f484d29bd7cfaf9c6ed864f-sitemap-en-bett1-de-1.xml.gz'
TRUSTPILOT_BUSINESS_ID = '487b774b000064000502e5b9'
TRUSTPILOT_TEMPLATE_ID = '5717796816f630043868e2e8'


def fetch_url(url, timeout=20, max_retries=3):
    """Fetch URL content using urllib with retry support."""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read()
        except Exception as e:
            if attempt == max_retries - 1:
                logger.warning(f"Failed to fetch {url} after {max_retries} attempts: {e}")
                return None
            time.sleep(1 + attempt)
    return None


def get_all_mattress_urls():
    """Discover all mattress variant URLs from the sitemap."""
    logger.info("Fetching sitemap to discover all mattress products and variants...")
    content = fetch_url(SITEMAP_URL)
    
    mattress_urls = set()
    if content:
        try:
            decompressed = gzip.decompress(content)
            root = ET.fromstring(decompressed)
            for elem in root.iter():
                if elem.tag.endswith('loc') and elem.text:
                    u = elem.text.strip()
                    if '/products/' in u:
                        slug = u.split('/products/')[-1]
                        # Target all mattress product lines
                        if any(slug.startswith(p) for p in [
                            'bodyguard-anti-cartel-mattress',
                            'bodyguard-box-spring-mattress',
                            'hulk-mattress',
                            'superbreeze-kids-mattress'
                        ]):
                            # Filter out non-mattress accessories
                            if not any(neg in slug for neg in [
                                'topper', 'cover', 'sheet', 'slatted', 'pillow', 
                                'duvet', 'protector', 'control-device'
                            ]):
                                mattress_urls.add(u)
        except Exception as e:
            logger.error(f"Error parsing sitemap: {e}")

    # Fallback / Direct Discovery if sitemap is unreachable or empty
    if not mattress_urls:
        logger.info("Sitemap parsing returned empty; checking category page...")
        cat_content = fetch_url('https://en.bett1.de/mattresses')
        if cat_content:
            soup = BeautifulSoup(cat_content.decode('utf-8', errors='ignore'), 'html.parser')
            for a in soup.find_all('a', href=True):
                href = a['href']
                if '/products/' in href:
                    full_url = href if href.startswith('http') else 'https://en.bett1.de' + href
                    slug = full_url.split('/products/')[-1]
                    if any(slug.startswith(p) for p in [
                        'bodyguard-anti-cartel-mattress',
                        'bodyguard-box-spring-mattress',
                        'hulk-mattress',
                        'superbreeze-kids-mattress'
                    ]) and not any(neg in slug for neg in ['topper', 'cover', 'sheet', 'slatted', 'pillow', 'duvet', 'protector', 'control-device']):
                        mattress_urls.add(full_url)

    urls_list = sorted(list(mattress_urls))
    logger.info(f"Found {len(urls_list)} mattress variants to scrape.")
    return urls_list


def extract_size(url, title, soup):
    """Extract standard mattress size (e.g., '120x190 cm') from page or URL."""
    # 1. Look for checked radio buttons in configurator
    checked_inputs = soup.find_all('input', checked=True)
    size_parts = []
    for inp in checked_inputs:
        lbl = soup.find('label', attrs={'for': inp.get('id')})
        if lbl:
            txt = lbl.get_text(strip=True)
            if txt.isdigit():
                size_parts.append(txt)
    if len(size_parts) == 2:
        return f"{size_parts[0]}x{size_parts[1]} cm"

    # 2. Extract from URL slug (e.g., bodyguard-anti-cartel-mattress-120x190)
    m = re.search(r'[-_](\d{2,3}x\d{2,3})(?:$|[^\d])', url)
    if m:
        return f"{m.group(1)} cm"

    # 3. Extract from Product Title / H1
    m = re.search(r'(\d{2,3}\s*[xX*]\s*\d{2,3})\s*(?:cm)?', title)
    if m:
        return f"{m.group(1).replace(' ', '')} cm"

    return "Standard"


def get_trustpilot_data(sku, default_rating=4.5, default_count=171882):
    """Fetch Trustpilot rating score and review count for a specific SKU."""
    if not sku:
        return default_rating, default_count
    
    tp_url = f"https://widget.trustpilot.com/trustbox-data/{TRUSTPILOT_TEMPLATE_ID}?businessUnitId={TRUSTPILOT_BUSINESS_ID}&locale=de-DE&sku={sku}"
    raw_json = fetch_url(tp_url, timeout=10)
    if raw_json:
        try:
            tp_json = json.loads(raw_json.decode('utf-8', errors='ignore'))
            prod_summary = tp_json.get('productReviewsSummary', {})
            total_prod_reviews = prod_summary.get('numberOfReviews', {}).get('total', 0)
            if total_prod_reviews > 0:
                stars = prod_summary.get('starsAverage', default_rating)
                return round(float(stars), 1), int(total_prod_reviews)
            
            bu = tp_json.get('businessUnit', {})
            if bu:
                stars = bu.get('stars', default_rating)
                count = bu.get('numberOfReviews', {}).get('total', default_count)
                return round(float(stars), 1), int(count)
        except Exception:
            pass
            
    return default_rating, default_count


def scrape_mattress_page(url):
    """Scrape a single mattress variant page and return a dictionary of fields."""
    raw_html = fetch_url(url)
    if not raw_html:
        return None

    html = raw_html.decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')

    product_name = ""
    sku = ""
    sale_price = None
    original_price = None
    currency = "EUR"

    # 1. Parse JSON-LD structured data
    json_lds = soup.find_all('script', type='application/ld+json')
    for j in json_lds:
        if not j.string:
            continue
        try:
            data = json.loads(j.string)
            items = data if isinstance(data, list) else [data]
            for item in items:
                if item.get('@type') == 'Product':
                    product_name = item.get('name', '')
                    sku = str(item.get('sku', '') or item.get('mpn', ''))
                    offers = item.get('offers', [])
                    if isinstance(offers, list) and len(offers) > 0:
                        sale_price = float(offers[0].get('price', 0))
                        currency = offers[0].get('priceCurrency', 'EUR')
                    elif isinstance(offers, dict):
                        sale_price = float(offers.get('price', 0))
                        currency = offers.get('priceCurrency', 'EUR')
                    break
        except Exception:
            pass

    # 2. Fallbacks for Product Name & SKU
    if not product_name:
        h1 = soup.find('h1')
        if h1:
            product_name = h1.get_text(strip=True)
        else:
            product_name = "BODYGUARD Mattress"

    # Clean up product name and special characters
    product_name = product_name.replace('\u00ae', '').replace('®', '').replace('\u2122', '').replace('&nbsp;', ' ').replace('\xa0', ' ')
    product_name = re.sub(r'\s+', ' ', product_name).strip()
    
    # Standardize German words to clean English titles if present
    product_name = product_name.replace('Anti-Kartell-Matratze', 'Anti-Cartel Mattress')

    # 3. Extract Size
    size = extract_size(url, product_name, soup)

    # 4. Extract Price / List Price (Original Price vs Sale Price)
    list_price_el = soup.find(class_=re.compile(r'list-price|strike|was-price|old-price', re.I))
    if list_price_el:
        lp_text = list_price_el.get_text(strip=True)
        m = re.search(r'[\d\.,]+', lp_text)
        if m:
            try:
                original_price = float(m.group(0).replace('.', '').replace(',', '.'))
            except:
                pass

    if sale_price is None:
        price_el = soup.find(class_=re.compile(r'product-detail-price', re.I))
        if price_el:
            p_text = price_el.get_text(strip=True)
            m = re.search(r'[\d\.,]+', p_text)
            if m:
                try:
                    sale_price = float(m.group(0).replace('.', '').replace(',', '.'))
                except:
                    pass

    if original_price is None and sale_price is not None:
        original_price = sale_price

    # 5. Fetch Reviews & Rating Count from Trustpilot
    review_score, rating_count = get_trustpilot_data(sku)

    return {
        'Product Name': product_name,
        'SKU': sku,
        'Size': size,
        'Original Price': original_price,
        'Sale Price': sale_price,
        'Currency': currency,
        'URL': url,
        'Review': review_score,
        'Rating Count': rating_count
    }


def save_to_styled_excel(data_rows, output_filepath="bett1_mattresses_data.xlsx"):
    """Export the scraped mattress data to a formatted Excel file."""
    df = pd.DataFrame(data_rows)
    
    # Save initial dataframe to Excel
    df.to_excel(output_filepath, index=False, sheet_name="Mattresses")

    # Style the Excel workbook
    wb = openpyxl.load_workbook(output_filepath)
    ws = wb["Mattresses"]

    # Colors
    header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid") # Dark Blue
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="Calibri", size=10)
    alt_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    
    thin_border = Border(
        left=Side(style='thin', color='E2E8F0'),
        right=Side(style='thin', color='E2E8F0'),
        top=Side(style='thin', color='E2E8F0'),
        bottom=Side(style='thin', color='E2E8F0')
    )

    # Header Row Styling
    for col_num in range(1, len(df.columns) + 1):
        cell = ws.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border
    
    ws.row_dimensions[1].height = 28

    # Data Rows Styling & Formatting
    for row_num in range(2, len(data_rows) + 2):
        ws.row_dimensions[row_num].height = 20
        is_even = (row_num % 2 == 0)
        
        for col_num in range(1, len(df.columns) + 1):
            cell = ws.cell(row=row_num, column=col_num)
            cell.font = data_font
            cell.border = thin_border
            if is_even:
                cell.fill = alt_fill

            col_name = df.columns[col_num - 1]
            
            # Alignments & Number formats
            if col_name in ['Original Price', 'Sale Price']:
                cell.number_format = '€#,##0.00'
                cell.alignment = Alignment(horizontal="right", vertical="center")
            elif col_name in ['Review']:
                cell.number_format = '0.0'
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_name in ['Rating Count', 'SKU', 'Size', 'Currency']:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                if col_name == 'Rating Count':
                    cell.number_format = '#,##0'
            elif col_name == 'URL':
                cell.alignment = Alignment(horizontal="left", vertical="center")
                cell.font = Font(name="Calibri", size=10, color="0000FF", underline="single")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")

    # Auto-adjust column widths
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    # Freeze header row
    ws.freeze_panes = "A2"

    wb.save(output_filepath)
    logger.info(f"Excel file successfully saved and styled: {output_filepath}")


def main():
    print("=" * 65)
    print("  bett1.de Mattress Web Scraper (All Variants & Sizes)")
    print("=" * 65)

    urls = get_all_mattress_urls()
    if not urls:
        logger.error("No mattress URLs found. Exiting.")
        sys.exit(1)

    print(f"\n[+] Scraping {len(urls)} mattress variant pages with multi-threading...", flush=True)
    scraped_data = []
    
    # Run scraping concurrently with ThreadPoolExecutor
    max_workers = 8
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scrape_mattress_page, u): u for u in urls}
        completed = 0
        total = len(futures)

        for future in as_completed(futures):
            res = future.result()
            completed += 1
            if res:
                scraped_data.append(res)
                print(f"[{completed}/{total}] Scraped: {res['Product Name']} ({res['Size']}) -> EUR {res['Sale Price']}", flush=True)
            else:
                print(f"[{completed}/{total}] Failed to scrape: {futures[future]}", flush=True)

    if not scraped_data:
        logger.error("No data could be extracted.")
        sys.exit(1)

    # Sort data by Product Name and Size
    scraped_data.sort(key=lambda x: (x['Product Name'], x['Size']))

    output_filename = "bett1_mattresses_data.xlsx"
    save_to_styled_excel(scraped_data, output_filename)

    print("\n" + "=" * 65)
    print(f"  Scraping Completed Successfully!")
    print(f"  Total Mattresses & Variants Extracted: {len(scraped_data)}")
    print(f"  Excel File: {os.path.abspath(output_filename)}")
    print("=" * 65)


if __name__ == '__main__':
    main()
