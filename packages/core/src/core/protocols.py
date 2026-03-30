"""Protocols for I/O boundaries used by the core service."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from core.models import Issue


@runtime_checkable
class IssueSource(Protocol):
    # Protocol keeps the boundary structural: duck-typed sources work without inheritance.
    def list_issues(self) -> Sequence[Issue]:
        """Return the current issue collection."""
