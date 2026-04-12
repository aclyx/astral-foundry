import pytest
from core import (
    CoreConfig,
    DigestRequest,
    InvalidIssueRequestError,
    IssueNotFoundError,
    IssueStatus,
)
from core.services import build_demo_service


def test_list_issues_filters_by_status_and_assignee() -> None:
    service = build_demo_service(CoreConfig(default_limit=10, source_name="demo"))

    digest = service.list_issues(
        DigestRequest(status=IssueStatus.OPEN, assignee="alex", limit=10),
    )

    assert digest.total == 2
    assert [issue.id for issue in digest.items] == ["ISS-101", "ISS-104"]

    digest = service.list_issues(
        DigestRequest(status=IssueStatus.BLOCKED),
    )

    assert digest.total == 1
    assert [issue.id for issue in digest.items] == ["ISS-106"]


def test_list_issues_uses_config_default_limit() -> None:
    service = build_demo_service(CoreConfig(default_limit=2, source_name="demo"))

    digest = service.list_issues()

    assert digest.total == 6
    assert digest.returned == 2


def test_get_issue_raises_for_missing_item() -> None:
    service = build_demo_service()

    with pytest.raises(IssueNotFoundError):
        service.get_issue("ISS-404")


def test_invalid_limit_is_rejected() -> None:
    service = build_demo_service()

    with pytest.raises(InvalidIssueRequestError):
        service.list_issues(DigestRequest(limit=0))


def test_label_filtering() -> None:
    service = build_demo_service(CoreConfig(source_name="demo"))

    digest = service.list_issues(DigestRequest(label="api", limit=10))

    assert digest.total == 1
    assert [issue.id for issue in digest.items] == ["ISS-104"]
