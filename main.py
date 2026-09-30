#!/usr/bin/env python3
"""
Speedtest Tracker — run internet speed tests, store history, show stats.

Usage:
    python main.py run           # Run a speed test
    python main.py history       # Show recent results
    python main.py stats         # Show min/max/avg stats
"""
import argparse

from tracker.runner import run_speedtest
from tracker.stats import print_history, print_stats
from tracker.storage import save_result


def cmd_run(db: str):
    print("Running speed test... (this may take 20-30 seconds)")
    result = run_speedtest()
    save_result(result, db)
    print(f"\nResults saved:")
    print(f"  Download : {result.download_mbps:.1f} Mbps")
    print(f"  Upload   : {result.upload_mbps:.1f} Mbps")
    print(f"  Ping     : {result.ping_ms:.1f} ms")
    print(f"  Server   : {result.server_name}, {result.server_country}\n")


def main():
    parser = argparse.ArgumentParser(description="Speedtest Tracker")
    parser.add_argument("--db", default="speedtest.db")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("run", help="Run a speed test and save results")

    p_hist = sub.add_parser("history", help="Show recent test history")
    p_hist.add_argument("-n", type=int, default=10, help="Number of results to show")

    sub.add_parser("stats", help="Show aggregate statistics")

    args = parser.parse_args()
    if args.cmd == "run":
        cmd_run(args.db)
    elif args.cmd == "history":
        print_history(args.n, args.db)
    elif args.cmd == "stats":
        print_stats(args.db)


if __name__ == "__main__":
    main()
