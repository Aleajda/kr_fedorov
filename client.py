import requests
import time

PAGES = list(range(1, 21))

urls = [
    "http://localhost:8081/parse",
    "http://localhost:8082/parse"
]

for url in urls:
    print(f"\n=== Тест {url} ===")
    start = time.time()

    r = requests.get(url, params={"pages": ",".join(map(str, PAGES))})
    print(r.json())

    print("Время запроса:", time.time() - start)