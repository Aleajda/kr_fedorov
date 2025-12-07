import asyncio
import os
import aiofiles

TEST_DIR = "test_files"

async def count_lines_in_file(path: str) -> int:
    count = 0
    async with aiofiles.open(path, "r") as f:
        async for _ in f:
            count += 1
    return count

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    filename = (await reader.read(1024)).decode().strip()
    filepath = os.path.join(TEST_DIR, filename)

    if not os.path.exists(filepath):
        writer.write(b"ERROR: file not found\n")
        await writer.drain()
        writer.close()
        return

    lines = await count_lines_in_file(filepath)
    writer.write(f"{lines}\n".format(lines).encode())
    await writer.drain()
    writer.close()

async def main():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 9001)
    print("Async server running on 9001")
    async with server:
        await server.serve_forever()

asyncio.run(main())
