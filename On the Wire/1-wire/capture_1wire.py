#!/usr/bin/env python3
import asyncio
import json
import ssl
import sys
from websockets import connect

URL = "wss://signals.holidayhackchallenge.com/wire/dq"
OUTFILE = "dq.csv"
TARGET = 10000

async def run():
    ssl_ctx = ssl.create_default_context()
    count = 0

    # open file in write mode, line-buffered
    # CSV header: line,t,v
    with open(OUTFILE, "w", buffering=1) as f:
        f.write("line,t,v\n")

        try:
            async with connect(URL, ssl=ssl_ctx) as ws:
                while count < TARGET:
                    raw = await ws.recv()            # wait for next message
                    try:
                        obj = json.loads(raw)
                    except json.JSONDecodeError:
                        # ignore non-JSON messages
                        continue

                    # require the three expected keys
                    if not all(k in obj for k in ("line", "t", "v")):
                        continue

                    # sanitize/convert
                    line = str(obj["line"])
                    try:
                        t = int(obj["t"])
                        v = int(obj["v"])
                    except (ValueError, TypeError):
                        continue

                    # write CSV row
                    f.write(f"{line},{t},{v}\n")
                    count += 1

                    # Progress indicator every 1000 rows
                    if count % 1000 == 0:
                        print(f"Collected {count}/{TARGET}")

        except Exception as e:
            print("Connection error or other exception:", e, file=sys.stderr)

    print(f"Done. Collected {count} messages into {OUTFILE}")

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
