from dataclasses import dataclass

from core import DigestRequest, Issue, IssueDigestService, IssueSource, IssueStatus


@dataclass(slots=True)
class DuckTypedSource:
    issues: tuple[Issue, ...]

    def list_issues(self) -> tuple[Issue, ...]:
        return self.issues


def test_protocol_accepts_duck_typed_source() -> None:
    issue = Issue(
        id="ISS-777",
        title="Duck typed source",
        status=IssueStatus.OPEN,
        summary="No inheritance is needed to satisfy the protocol.",
    )
    source = DuckTypedSource(issues=(issue,))
    service = IssueDigestService(source)

    assert isinstance(source, IssueSource)
    digest = service.list_issues(DigestRequest(limit=10))
    assert [item.id for item in digest.items] == ["ISS-777"]
