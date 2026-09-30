"""Run a speedtest and return structured results."""
from dataclasses import dataclass, field
from datetime import datetime

try:
    import speedtest as _speedtest_lib
except ImportError:
    _speedtest_lib = None  # type: ignore[assignment]


@dataclass
class SpeedResult:
    download_mbps: float
    upload_mbps: float
    ping_ms: float
    server_name: str
    server_country: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


def run_speedtest() -> SpeedResult:
    """Run a real speedtest using the speedtest-cli library."""
    if _speedtest_lib is None:
        raise RuntimeError("Install speedtest-cli: pip install speedtest-cli")

    st = _speedtest_lib
    s = st.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    res = s.results.dict()

    return SpeedResult(
        download_mbps=round(res["download"] / 1_000_000, 2),
        upload_mbps=round(res["upload"] / 1_000_000, 2),
        ping_ms=round(res["ping"], 2),
        server_name=res["server"]["name"],
        server_country=res["server"]["country"],
    )
