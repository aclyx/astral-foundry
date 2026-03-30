"""Configuration helpers for the shared core package."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from core.errors import ConfigurationError


@dataclass(slots=True, frozen=True)
class CoreConfig:
    default_limit: int = 5
    source_name: str = "local-demo"

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> Self:
        values = os.environ if env is None else env
        default_limit = _parse_positive_int(
            values.get("ISSUE_DIGEST_DEFAULT_LIMIT"),
            name="ISSUE_DIGEST_DEFAULT_LIMIT",
            default=5,
        )
        source_name = values.get("ISSUE_DIGEST_SOURCE_NAME", "local-demo").strip() or "local-demo"
        return cls(default_limit=default_limit, source_name=source_name)


def _parse_positive_int(raw: str | None, *, name: str, default: int) -> int:
    if raw is None:
        return default

    try:
        value = int(raw)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be an integer") from exc

    if value <= 0:
        raise ConfigurationError(f"{name} must be greater than zero")
    return value
