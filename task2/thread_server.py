import os
import socket
from concurrent.futures import ThreadPoolExecutor

TEST_DIR = "test_files"

def count_lines_in_file(path: str) -> int:
    with open(path, "r") as f:
        return sum(1 for _ in f)

def handle_connection(conn):
    filename = conn.recv(1024).decode().strip()
    filepath = os.path.join(TEST_DIR, filename)

    if not os.path.exists(filepath):
        conn.send(b"ERROR: file not found\n")
        conn.close()
        return

    lines = count_lines_in_file(filepath)
    conn.send(f"{lines}\n".encode())
    conn.close()

def main():
    executor = ThreadPoolExecutor(max_workers=200)
    sock = socket.socket()
    sock.bind(("127.0.0.1", 9002))
    sock.listen(200)
    print("Thread server running on 9002")

    while True:
        conn, _ = sock.accept()
        executor.submit(handle_connection, conn)

main()
