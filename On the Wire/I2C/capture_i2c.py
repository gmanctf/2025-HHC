import asyncio
import json
import websockets

async def capture_line(name, url, outfile):
    """
    Connect to SDA or SCL websocket and capture:
    - all packets starting from the first t == 0
    - until the next t == 0 (inclusive)
    """

    print(f"[+] Connecting to {name.upper()} at {url} ...")

    buffer = []
    started = False

    try:
        async with websockets.connect(url) as ws:
            print(f"[+] Connected to {name.upper()}")

            while True:
                msg = await ws.recv()

                try:
                    pkt = json.loads(msg)
                except Exception:
                    continue

                if pkt.get("line") != name:
                    continue

                t = pkt.get("t")

                # First t == 0 → start capture
                if t == 0 and not started:
                    print(f"[+] First timestamp=0 for {name.upper()} detected — starting capture")
                    started = True
                    buffer.append(pkt)
                    continue

                if started:
                    buffer.append(pkt)

                    # Second t == 0 → stop capture
                    if t == 0 and len(buffer) > 1:
                        print(f"[+] Second timestamp=0 for {name.upper()} detected — finishing capture")
                        break

    except asyncio.CancelledError:
        print(f"[!] {name.upper()} capture cancelled (Ctrl+C)")
        # re-raise so asyncio knows the task was cancelled
        raise

    finally:
        # write data, even if cancelled
        if buffer:
            with open(outfile, "w") as f:
                for entry in buffer:
                    f.write(json.dumps(entry) + "\n")

            print(f"[+] Saved {len(buffer)} packets to {outfile}")
        else:
            print(f"[!] No packets captured for {name.upper()}")

async def main():
    await asyncio.gather(
        capture_line(
            "sda",
            "wss://signals.holidayhackchallenge.com/wire/sda",
            "sda.json"
        ),
        capture_line(
            "scl",
            "wss://signals.holidayhackchallenge.com/wire/scl",
            "scl.json"
        )
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[+] Capture interrupted by user — exiting cleanly")
