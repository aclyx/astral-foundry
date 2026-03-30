from datetime import UTC, datetime

from core.models import DigestRequest, Issue, IssueDigest, IssueStatus


def test_issue_matches_search_across_multiple_fields() -> None:
    issue = Issue(
        id="ISS-999",
        title="Teach protocol-based sources",
        status=IssueStatus.OPEN,
        summary="Use structural typing instead of a hard inheritance tree.",
        assignee="Taylor",
        labels=("typing", "learning"),
        created_at=datetime(2026, 3, 29, 10, 0, tzinfo=UTC),
        updated_at=datetime(2026, 3, 29, 10, 0, tzinfo=UTC),
    )

    assert issue.matches_search("protocol")
    assert issue.matches_search("taylor")
    assert issue.matches_search("typing")
    assert not issue.matches_search("database")


def test_issue_digest_reports_returned_count() -> None:
    issue = Issue(
        id="ISS-100",
        title="One item",
        status=IssueStatus.OPEN,
        summary="Minimal digest item.",
    )

    digest = IssueDigest(request=DigestRequest(limit=10), total=1, items=(issue,))

    assert digest.returned == 1
