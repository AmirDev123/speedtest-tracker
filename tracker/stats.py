"""Calculate statistics over stored speedtest results."""
from .storage import fetch_all


def compute_stats(db_path: str = "speedtest.db") -> dict | None:
    rows = fetch_all(limit=1000, db_path=db_path)
    if not rows:
        return None

    def _stat(key: str) -> dict:
        vals = [r[key] for r in rows]
        return {
            "min": round(min(vals), 2),
            "max": round(max(vals), 2),
            "avg": round(sum(vals) / len(vals), 2),
            "latest": round(vals[0], 2),
        }

    return {
        "count": len(rows),
        "download_mbps": _stat("download_mbps"),
        "upload_mbps": _stat("upload_mbps"),
        "ping_ms": _stat("ping_ms"),
    }


def print_history(limit: int = 10, db_path: str = "speedtest.db") -> None:
    rows = fetch_all(limit=limit, db_path=db_path)
    if not rows:
        print("No results yet. Run: python main.py run")
        return
    print(f"\n{'Timestamp':<26} {'Down':>8}  {'Up':>8}  {'Ping':>7}  Server")
    print("─" * 75)
    for r in rows:
        print(
            f"{r['timestamp']:<26} {r['download_mbps']:>7.1f}M  "
            f"{r['upload_mbps']:>7.1f}M  {r['ping_ms']:>6.1f}ms  "
            f"{r['server_name']}, {r['server_country']}"
        )
    print()


def print_stats(db_path: str = "speedtest.db") -> None:
    stats = compute_stats(db_path)
    if not stats:
        print("No results yet.")
        return
    print(f"\nStatistics over {stats['count']} test(s):")
    for metric, label in [("download_mbps", "Download"), ("upload_mbps", "Upload"), ("ping_ms", "Ping")]:
        s = stats[metric]
        unit = "ms" if metric == "ping_ms" else "Mbps"
        print(f"  {label:<10}  latest={s['latest']:>8.1f}{unit}  "
              f"avg={s['avg']:>8.1f}{unit}  min={s['min']:>8.1f}{unit}  max={s['max']:>8.1f}{unit}")
    print()
