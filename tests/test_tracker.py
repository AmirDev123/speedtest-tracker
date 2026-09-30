import tempfile
import unittest
from unittest.mock import MagicMock, patch

from tracker.runner import SpeedResult
from tracker.stats import compute_stats
from tracker.storage import fetch_all, save_result


def _make_result(down=100.0, up=50.0, ping=10.0):
    return SpeedResult(
        download_mbps=down,
        upload_mbps=up,
        ping_ms=ping,
        server_name="Test Server",
        server_country="Norway",
    )


class TestStorage(unittest.TestCase):
    def _db(self):
        return tempfile.mktemp(suffix=".db")

    def test_save_and_fetch(self):
        db = self._db()
        save_result(_make_result(), db)
        rows = fetch_all(db_path=db)
        self.assertEqual(len(rows), 1)
        self.assertAlmostEqual(rows[0]["download_mbps"], 100.0)

    def test_multiple_results_ordered_desc(self):
        db = self._db()
        r1 = _make_result(50.0)
        r1.timestamp = "2024-01-01T00:00:00"
        r2 = _make_result(80.0)
        r2.timestamp = "2024-01-02T00:00:00"
        save_result(r1, db)
        save_result(r2, db)
        rows = fetch_all(db_path=db)
        self.assertGreater(rows[0]["timestamp"], rows[1]["timestamp"])

    def test_limit_is_respected(self):
        db = self._db()
        for _ in range(5):
            save_result(_make_result(), db)
        rows = fetch_all(limit=3, db_path=db)
        self.assertEqual(len(rows), 3)


class TestStats(unittest.TestCase):
    def _db(self):
        return tempfile.mktemp(suffix=".db")

    def test_no_data_returns_none(self):
        db = self._db()
        self.assertIsNone(compute_stats(db))

    def test_single_result(self):
        db = self._db()
        save_result(_make_result(100.0, 50.0, 10.0), db)
        stats = compute_stats(db)
        self.assertEqual(stats["count"], 1)
        self.assertAlmostEqual(stats["download_mbps"]["avg"], 100.0)

    def test_avg_is_correct(self):
        db = self._db()
        save_result(_make_result(down=40.0), db)
        save_result(_make_result(down=60.0), db)
        stats = compute_stats(db)
        self.assertAlmostEqual(stats["download_mbps"]["avg"], 50.0)

    def test_min_max(self):
        db = self._db()
        for v in [20.0, 80.0, 50.0]:
            save_result(_make_result(down=v), db)
        stats = compute_stats(db)
        self.assertAlmostEqual(stats["download_mbps"]["min"], 20.0)
        self.assertAlmostEqual(stats["download_mbps"]["max"], 80.0)


class TestRunner(unittest.TestCase):
    @patch("tracker.runner._speedtest_lib")
    def test_run_speedtest_returns_speed_result(self, mock_st_module):
        mock_instance = MagicMock()
        mock_st_module.Speedtest.return_value = mock_instance
        mock_instance.results.dict.return_value = {
            "download": 100_000_000,
            "upload": 50_000_000,
            "ping": 12.5,
            "server": {"name": "Oslo", "country": "Norway"},
        }
        from tracker.runner import run_speedtest
        result = run_speedtest()
        self.assertAlmostEqual(result.download_mbps, 100.0)
        self.assertAlmostEqual(result.upload_mbps, 50.0)
        self.assertAlmostEqual(result.ping_ms, 12.5)


if __name__ == "__main__":
    unittest.main()
