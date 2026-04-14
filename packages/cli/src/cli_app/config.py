"""Configuration loading for the CLI package."""

from __future__ import annotations

import os
import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, Self, cast

from core.errors import ConfigurationError

OutputFormat = Literal["text", "json"]
DEFAULT_CONFIG_FILE = ".astral-foundry.toml"


@dataclass(slots=True, frozen=True)
class CliConfig:
    api_base_url: str = "http://127.0.0.1:8000"
    default_output: OutputFormat = "text"
    timeout_seconds: float = 5.0
    config_path: Path | None = None

    @classmethod
    def from_env(
        cls,
        env: Mapping[str, str] | None = None,
        *,
        cwd: Path | None = None,
        config_path: Path | None = None,
    ) -> Self:
        values = os.environ if env is None else env
        root = Path.cwd() if cwd is None else cwd
        resolved_path = _resolve_config_path(values, root=root, override=config_path)
        file_config = _read_config_file(resolved_path)

        api_base_url = str(
            values.get("ISSUE_DIGEST_API_URL") or file_config.get("api_base_url") or "http://127.0.0.1:8000",
        ).rstrip("/")
        default_output = _parse_output_format(
            values.get("ISSUE_DIGEST_OUTPUT") or file_config.get("default_output") or "text",
        )
        timeout_seconds = _parse_timeout(
            values.get("ISSUE_DIGEST_TIMEOUT_SECONDS") or file_config.get("timeout_seconds"),
        )

        return cls(
            api_base_url=api_base_url,
            default_output=default_output,
            timeout_seconds=timeout_seconds,
            config_path=resolved_path if resolved_path.exists() else None,
        )


def _resolve_config_path(
    env: Mapping[str, str],
    *,
    root: Path,
    override: Path | None,
) -> Path:
    if override is not None:
        return override.expanduser()

    configured = env.get("ISSUE_DIGEST_CONFIG_FILE")
    if configured:
        return Path(configured).expanduser()
    return root / DEFAULT_CONFIG_FILE


def _read_config_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}

    # Python 3.11+ ships tomllib, so a small local config file does not need another dependency.
    data = tomllib.loads(path.read_text())
    cli_config = data.get("cli")
    if cli_config is None:
        return {}
    if not isinstance(cli_config, dict):
        raise ConfigurationError("the [cli] section in the config file must be a table")
    return cli_config


def _parse_output_format(raw: str) -> OutputFormat:
    if raw not in {"text", "json"}:
        raise ConfigurationError("ISSUE_DIGEST_OUTPUT must be 'text' or 'json'")
    return cast(OutputFormat, raw)


def _parse_timeout(raw: str | float | int | None) -> float:
    if raw is None:
        return 5.0
    try:
        value = float(raw)
    except (TypeError, ValueError) as exc:
        raise ConfigurationError("ISSUE_DIGEST_TIMEOUT_SECONDS must be a number") from exc
    if value <= 0:
        raise ConfigurationError("ISSUE_DIGEST_TIMEOUT_SECONDS must be greater than zero")
    return value
