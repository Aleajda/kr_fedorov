import asyncio
import socket
import time
import psutil
import random
import os

TEST_DIR = "test_files"
FILES = os.listdir(TEST_DIR)

async def async_request():
    reader, writer = await asyncio.open_connection("127.0.0.1", 9001)
    name = random.choice(FILES)
    writer.write(name.encode())
    await writer.drain()
    await reader.readline()
    writer.close()

async def run_async_load(n):
    tasks = [asyncio.create_task(async_request()) for _ in range(n)]
    await asyncio.gather(*tasks)

def thread_request():
    s = socket.socket()
    s.connect(("127.0.0.1", 9002))
    name = random.choice(FILES)
    s.send(name.encode())
    s.recv(1024)
    s.close()

def run_thread_load(n):
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=n) as ex:
        for _ in range(n):
            ex.submit(thread_request)


def measure(fn, n, label):
    print(f"\n=== {label}: {n} concurrent requests ===")
    p = psutil.Process()

    mem_before = p.memory_info().rss / 1024 / 1024
    t0 = time.time()
    fn(n)
    dt = time.time() - t0
    mem_after = p.memory_info().rss / 1024 / 1024

    print(f"Time: {dt:.2f} sec")
    print(f"Memory used: {mem_after - mem_before:.2f} MB")


if __name__ == "__main__":
    N = 1000

    measure(lambda n: asyncio.run(run_async_load(n)), N, "AsyncIO server")

    measure(run_thread_load, N, "Thread server")
