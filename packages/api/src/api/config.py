"""Configuration for the API package."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from core.errors import ConfigurationError


@dataclass(slots=True, frozen=True)
class ApiConfig:
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = False

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> Self:
        values = os.environ if env is None else env
        host = values.get("API_HOST", "127.0.0.1").strip() or "127.0.0.1"
        port = _parse_port(values.get("API_PORT"))
        debug = _parse_bool(values.get("API_DEBUG"), default=False)
        return cls(host=host, port=port, debug=debug)


def _parse_port(raw: str | None) -> int:
    if raw is None:
        return 8000
    try:
        value = int(raw)
    except ValueError as exc:
        raise ConfigurationError("API_PORT must be an integer") from exc
    if value <= 0:
        raise ConfigurationError("API_PORT must be greater than zero")
    return value


def _parse_bool(raw: str | None, *, default: bool) -> bool:
    if raw is None:
        return default
    normalized = raw.strip().casefold()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ConfigurationError("API_DEBUG must be a boolean value")
