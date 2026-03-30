"""Shared domain models and services for the issue digest workspace."""

from core.config import CoreConfig
from core.errors import (
    ConfigurationError,
    InvalidIssueRequestError,
    IssueDigestError,
    IssueNotFoundError,
    SourceUnavailableError,
)
from core.models import DigestRequest, Issue, IssueDigest, IssueStatus
from core.protocols import IssueSource
from core.services import InMemoryIssueSource, IssueDigestService, build_demo_service

__all__ = [
    "ConfigurationError",
    "CoreConfig",
    "DigestRequest",
    "InMemoryIssueSource",
    "InvalidIssueRequestError",
    "Issue",
    "IssueDigest",
    "IssueDigestError",
    "IssueDigestService",
    "IssueNotFoundError",
    "IssueSource",
    "IssueStatus",
    "SourceUnavailableError",
    "build_demo_service",
]
