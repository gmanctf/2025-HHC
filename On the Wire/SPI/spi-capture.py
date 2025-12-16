#!/usr/bin/env python3
import asyncio
import json
import websockets
from pathlib import Path

URL_MOSI = "wss://signals.holidayhackchallenge.com/wire/mosi"
URL_SCK  = "wss://signals.holidayhackchallenge.com/wire/sck"

OUT_MOSI = "mosi.json"
OUT_SCK  = "sck.json"

async def capture_line(url, out_path, line_name):
    """
    Connect to a single WSS line (MOSI or SCK)
    Capture packets from first idle-low to next idle-low.
    """
    p = Path(out_path)
    if p.exists():
        p.unlink()

    print(f"[{line_name}] Connecting to {url} ...")

    async with websockets.connect(url) as ws:
        print(f"[{line_name}] Connected. Waiting for first idle-low...")

        idle_seen = False
        started = False
        finished = False

        with open(out_path, "w") as fh:

            async for msg in ws:
                try:
                    pkt = json.loads(msg)
                except Exception:
                    pkt = {"line": line_name, "raw": msg}

                pkt["line"] = line_name

                marker = pkt.get("marker")

                # Wait for first idle-low
                if not idle_seen:
                    if marker == "idle-low":
                        idle_seen = True
                        started = True
                        fh.write(json.dumps(pkt) + "\n")
                        fh.flush()
                        print(f"[{line_name}] First idle-low → starting capture")
                    continue

                fh.write(json.dumps(pkt) + "\n")
                fh.flush()

                # End capture on next idle-low
                if marker == "idle-low":
                    print(f"[{line_name}] Second idle-low → capture complete")
                    finished = True
                    break

        if not finished:
            print(f"[{line_name}] WARNING: stream closed before second idle-low.")
        else:
            print(f"[{line_name}] Saved capture to {out_path}")


async def main():
    task_mosi = asyncio.create_task(capture_line(URL_MOSI, OUT_MOSI, "mosi"))
    task_sck  = asyncio.create_task(capture_line(URL_SCK,  OUT_SCK,  "sck"))

    await asyncio.gather(task_mosi, task_sck)
    print("[+] Both captures complete.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
