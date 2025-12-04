
import asyncio
from aiohttp import web, ClientSession
from bs4 import BeautifulSoup
import time
from config import URLS

async def fetch(session, url):
    try:
        async with session.get(url) as r:
            if r.status == 200:
                return await r.text()
    except:
        return None


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.select('div.set-card')

    names = []
    total = 0.0

    for c in cards:
        t = c.select_one('.set-card__title a')
        if not t:
            continue
        names.append(t.get_text(strip=True))

        pm = c.select_one('meta[itemprop="price"]')
        total += float(pm['content']) if pm else 0

    return names, total


async def handle_parse(request):
    start = time.time()

    async with ClientSession() as session:
        tasks = [fetch(session, url) for url in URLS]
        html_list = await asyncio.gather(*tasks)

    all_names = []
    total_sum = 0

    for html in html_list:
        if html:
            names, s = parse(html)
            all_names.extend(names)
            total_sum += s

    with open("async_server_output.txt", "a", encoding="utf8") as f:
        for n in all_names:
            f.write(n + "")

    return web.json_response({
        "parsed": len(all_names),
        "sum": total_sum,
        "time": time.time() - start
    })


app = web.Application()
app.router.add_get('/parse', handle_parse)

if __name__ == '__main__':
    web.run_app(app, port=8081)