from core import IssueNotFoundError, build_demo_service


def main() -> int:
    service = build_demo_service()
    try:
        service.get_issue("ISS-404")
    except IssueNotFoundError as exc:
        # Expected domain errors are handled locally so failures stay user-readable.
        print(f"recoverable error: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
