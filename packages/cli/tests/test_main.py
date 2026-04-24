import json
from pathlib import Path

from cli_app.main import run


def test_items_list_json_output(capsys) -> None:
    exit_code = run(["items", "list", "--output", "json", "--limit", "2"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert exit_code == 0
    assert payload["returned"] == 2
    assert captured.err == ""


def test_items_list_with_label_filter(capsys) -> None:
    exit_code = run(["items", "list", "--label", "api", "--limit", "10"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert exit_code == 0
    assert payload["returned"] == 1
    assert payload["items"][0]["id"] == "ISS-104"


def test_cli_reads_local_config_file(tmp_path: Path, monkeypatch, capsys) -> None:
    config_path = tmp_path / ".astral-foundry.toml"
    config_path.write_text(
        "[cli]\napi_base_url = 'http://localhost:9000'\ndefault_output = 'json'\ntimeout_seconds = 3.0\n",
    )
    monkeypatch.chdir(tmp_path)

    exit_code = run(["health"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["api_base_url"] == "http://localhost:9000"
