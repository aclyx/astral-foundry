"""Domain-specific exceptions for the issue digest workspace."""


class IssueDigestError(Exception):
    """Base exception for expected domain and integration failures."""


class ConfigurationError(IssueDigestError):
    """Raised when environment or local configuration is invalid."""


class InvalidIssueRequestError(IssueDigestError):
    """Raised when a filter request cannot be satisfied."""


class IssueNotFoundError(IssueDigestError):
    """Raised when the requested issue does not exist in the current source."""

    def __init__(self, issue_id: str) -> None:
        super().__init__(f"issue {issue_id!r} was not found")
        self.issue_id = issue_id


class SourceUnavailableError(IssueDigestError):
    """Raised when an external or remote issue source cannot be reached."""
