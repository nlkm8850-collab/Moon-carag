import argparse
import csv
import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def clean_price(value: str) -> float:
    value = value.replace(",", "").replace(" ", "")
    match = re.search(r"(\d+(?:\.\d+)?)", value)
    if not match:
        raise ValueError(f"Could not parse price from: {value}")
    return float(match.group(1))


def extract_price_from_html(html: str, selector: Optional[str] = None) -> Optional[float]:
    soup = BeautifulSoup(html, "html.parser")

    if selector:
        element = soup.select_one(selector)
        if element:
            text = element.get_text(" ", strip=True)
            try:
                return clean_price(text)
            except ValueError:
                pass

    for tag in soup.find_all(string=True):
        if not isinstance(tag, str):
            continue
        text = tag.strip()
        if not text:
            continue
        try:
            return clean_price(text)
        except ValueError:
            pass

    return None


def load_products(config_path: str) -> List[Dict]:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Configuration must be a JSON list of products")
    return data


def fetch_html(url: str) -> str:
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=20)
    response.raise_for_status()
    return response.text


def append_log(rows: List[Dict], path: str) -> None:
    file_path = Path(path)
    fieldnames = [
        "timestamp",
        "name",
        "url",
        "competitor_price",
        "your_price",
        "price_diff_pct",
        "status",
    ]

    if not file_path.exists():
        with file_path.open("w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    with file_path.open("a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for row in rows:
            writer.writerow(row)


def monitor(products: List[Dict], interval_seconds: int, threshold: float, log_path: str) -> None:
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        batch_rows: List[Dict] = []

        for product in products:
            name = product.get("name", "Unnamed Product")
            url = product["url"]
            your_price = float(product["your_price"])
            selector = product.get("selector")

            try:
                html = fetch_html(url)
                competitor_price = extract_price_from_html(html, selector)

                if competitor_price is None:
                    status = "PRICE_NOT_FOUND"
                    price_diff_pct = None
                else:
                    if your_price <= 0:
                        status = "INVALID_YOUR_PRICE"
                        price_diff_pct = None
                    else:
                        price_diff_pct = ((your_price - competitor_price) / your_price) * 100
                        if competitor_price < your_price * (1 - threshold):
                            status = "PRICE_DROP_ALERT"
                        else:
                            status = "OK"

                row = {
                    "timestamp": now,
                    "name": name,
                    "url": url,
                    "competitor_price": competitor_price if competitor_price is not None else "",
                    "your_price": your_price,
                    "price_diff_pct": "" if price_diff_pct is None else round(price_diff_pct, 2),
                    "status": status,
                }

                batch_rows.append(row)

                if status == "PRICE_DROP_ALERT":
                    print(
                        f"[ALERT] {name} | Competitor: {competitor_price} | Your price: {your_price} | "
                        f"Difference: {price_diff_pct:.2f}%"
                    )
                else:
                    print(f"[INFO] {name} | Status: {status} | Price: {competitor_price}")

            except Exception as exc:
                print(f"[ERROR] {name} | {exc}")
                batch_rows.append(
                    {
                        "timestamp": now,
                        "name": name,
                        "url": url,
                        "competitor_price": "",
                        "your_price": your_price,
                        "price_diff_pct": "",
                        "status": "ERROR",
                    }
                )

        append_log(batch_rows, log_path)
        print(f"[INFO] Scan completed at {now}. Waiting {interval_seconds} seconds...")
        time.sleep(interval_seconds)


def main() -> None:
    parser = argparse.ArgumentParser(description="Monitor competitor prices and alert on major drops.")
    parser.add_argument("--config", required=True, help="Path to JSON product list")
    parser.add_argument("--interval", type=int, default=1800, help="Check interval in seconds")
    parser.add_argument("--threshold", type=float, default=0.10, help="Alert threshold as decimal fraction, e.g., 0.10 = 10%")
    parser.add_argument("--log", default="price_monitor_log.csv", help="CSV log output path")
    args = parser.parse_args()

    products = load_products(args.config)
    monitor(products, args.interval, args.threshold, args.log)


if __name__ == "__main__":
    main()
