import argparse
import os
import sys

import uvicorn


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--reload", action="store_true")
    return parser.parse_args()


def main():
    print(r"""
        .__            .___
  _____ |  |_______  __| _/
 /     \|  |\_  __ \/ __ |
|  Y Y  \  |_|  | \/ /_/ |
|__|_|  /____/__|  \____ |
      \/                \/
2022 MLRD by rapsealk
    """)

    args = parse_args()

    if sys.platform == "win32":
        workers = 1
    else:
        workers = args.workers or min(os.cpu_count() + 1, 32)

    uvicorn.run("mlrd.main:app", host=args.host, port=args.port, workers=workers, reload=args.reload)


if __name__ == "__main__":
    main()
