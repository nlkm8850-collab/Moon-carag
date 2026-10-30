# Competitor Price Monitor

A lightweight monitoring tool for online businesses that tracks competitor prices and alerts you when a product drops below your target threshold.

## What it does
- Loads products from a JSON config file
- Fetches competitor product pages
- Extracts prices from HTML
- Compares them against your configured prices
- Logs results to CSV
- Sends alerts when a competitor drops price beyond your threshold

## Files
- `price_monitor.py` — main monitoring script
- `requirements.txt` — Python dependencies
- `products.example.json` — example product list
- `README.md` — usage instructions

## Quick start

1. Install dependencies
```bash
pip install -r requirements.txt
```

2. Copy the example config
```bash
cp products.example.json products.json
```

3. Edit `products.json` with your products
4. Run the monitor
```bash
python price_monitor.py --config products.json --interval 1800 --threshold 0.10
```

## Example configuration
```json
[
  {
    "name": "Samsung Galaxy S24",
    "url": "https://example.com/product/1",
    "your_price": 2999,
    "selector": ".price"
  }
]
```

## Notes
- Some websites block scrapers; use a realistic user-agent and rotate IPs if needed.
- For JavaScript-heavy stores, consider Playwright or Selenium for stronger extraction.
- This is a practical MVP for competitor price intelligence.
