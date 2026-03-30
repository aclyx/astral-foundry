from core import DigestRequest, IssueStatus, build_demo_service


def main() -> int:
    # A tiny main() keeps side effects local and mirrors
    # how small Python scripts are usually structured.
    service = build_demo_service()
    digest = service.list_issues(DigestRequest(status=IssueStatus.OPEN, limit=3))

    for issue in digest.items:
        print(f"{issue.id}: {issue.title}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
