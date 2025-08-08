import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from snb_prometheus.backfill import backfill
from snb_prometheus.config import Config


def test_backfill_invokes_promtool(monkeypatch, tmp_path):
    csv_text = Path("tests/data/sample_indicator.csv").read_text()

    def fake_fetch_csv(cube, language="en", params=None):
        assert cube == "monzano"
        assert params == {"filter[KEYSERIES]": "A.POLIRATE"}
        return csv_text

    monkeypatch.setattr("snb_prometheus.backfill.fetch_csv", fake_fetch_csv)

    recorded = {}

    def fake_run(cmd, check):
        recorded["cmd"] = cmd
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(subprocess, "run", fake_run)

    cfg = Config(indicators={"policy_rate": ("monzano", "A.POLIRATE")})
    backfill(cfg, tsdb_path=str(tmp_path))

    cmd = recorded["cmd"]
    assert cmd[:4] == ["promtool", "tsdb", "create-blocks-from", "openmetrics"]
    metrics_file = Path(cmd[4])
    content = metrics_file.read_text().splitlines()
    assert content[0] == "# TYPE snb_indicator_value gauge"
    ts1 = int(datetime.fromisoformat("2023-01-01").timestamp())
    ts2 = int(datetime.fromisoformat("2023-02-01").timestamp())
    assert (
        content[1]
        == f'snb_indicator_value{{indicator="policy_rate"}} 1.0 {ts1}'
    )
    assert (
        content[2]
        == f'snb_indicator_value{{indicator="policy_rate"}} 1.5 {ts2}'
    )


def test_main_backfill(monkeypatch):
    calls = []
    monkeypatch.setattr("snb_prometheus.main.run_server", lambda: calls.append("server"))
    monkeypatch.setattr("snb_prometheus.main.backfill", lambda: calls.append("backfill"))

    import sys

    monkeypatch.setattr(sys, "argv", ["prog", "--backfill"])
    from snb_prometheus import main as main_mod

    main_mod.main()
    assert calls == ["backfill", "server"]
