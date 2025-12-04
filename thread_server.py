from flask import Flask, jsonify
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
import time
from config import URLS

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=10)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def fetch(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        return r.text if r.status_code == 200 else None
    except:
        return None


def parse(html):
    if not html:
        return [], 0.0

    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("div.set-card")

    names = []
    total = 0.0

    for card in cards:
        t = card.select_one(".set-card__title a")
        if not t:
            continue
        names.append(t.get_text(strip=True))

        price_tag = card.select_one('meta[itemprop="price"]')
        if price_tag and price_tag.get("content"):
            total += float(price_tag["content"])

    return names, total


def worker(url):
    html = fetch(url)
    if not html:
        return [], 0.0
    return parse(html)


@app.get("/parse")
def handle_parse():
    start = time.time()

    futures = [executor.submit(worker, url) for url in URLS]

    all_names = []
    grand_total = 0.0

    for fut in as_completed(futures):
        names, total = fut.result()
        all_names.extend(names)
        grand_total += total

    with open("thread_server_output.txt", "a", encoding="utf8") as f:
        for n in all_names:
            f.write(n + "\n")

    return jsonify({
        "parsed": len(all_names),
        "sum": grand_total,
        "time": time.time() - start
    })


if __name__ == "__main__":
    app.run(port=8082)
