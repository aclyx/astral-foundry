from dataclasses import dataclass

from core import Issue, IssueDigestService, IssueStatus


@dataclass(slots=True)
class SingleIssueSource:
    issue: Issue

    def list_issues(self) -> tuple[Issue, ...]:
        return (self.issue,)


def main() -> None:
    issue = Issue(
        id="ISS-500",
        title="Demonstrate protocol-based source swapping",
        status=IssueStatus.OPEN,
        summary="A concrete source only needs the right method shape.",
    )
    # The service cares about the behavior contract, not a shared base class.
    service = IssueDigestService(SingleIssueSource(issue))
    digest = service.list_issues()
    print(digest.items[0].title)


if __name__ == "__main__":
    main()
