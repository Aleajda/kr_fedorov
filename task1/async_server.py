import asyncio
from aiohttp import web, ClientSession
from bs4 import BeautifulSoup
import time
import os
import psutil
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
    process = psutil.Process(os.getpid())
    cpu_start = process.cpu_times()
    mem_start = process.memory_info().rss

    start_time = time.time()

    async with ClientSession() as session:
        tasks = [fetch(session, url) for url in URLS]
        html_list = await asyncio.gather(*tasks)

    all_names = []
    total_sum = 0.0

    for html in html_list:
        if html:
            names, s = parse(html)
            all_names.extend(names)
            total_sum += s

    with open("async_server_output.txt", "a", encoding="utf8") as f:
        for n in all_names:
            f.write(n + "\n")

    cpu_end = process.cpu_times()
    mem_end = process.memory_info().rss

    cpu_used = (cpu_end.user + cpu_end.system) - (cpu_start.user + cpu_start.system)
    mem_used_mb = (mem_end - mem_start) / 1024 / 1024

    return web.json_response({
        "parsed": len(all_names),
        "sum": total_sum,
        "time": time.time() - start_time,
        "cpu_seconds": round(cpu_used, 4),
        "memory_mb": round(mem_used_mb, 2)
    })


app = web.Application()
app.router.add_get('/parse', handle_parse)

if __name__ == '__main__':
    web.run_app(app, port=8081)
