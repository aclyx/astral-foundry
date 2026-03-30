from contextlib import contextmanager
from time import perf_counter

from core import build_demo_service


@contextmanager
def timed(label: str):
    started_at = perf_counter()
    try:
        yield
    finally:
        duration = perf_counter() - started_at
        print(f"{label}: {duration:.4f}s")


def main() -> None:
    service = build_demo_service()
    # Context managers keep setup and teardown in one local scope
    # instead of scattering cleanup code.
    with timed("list open issues"):
        digest = service.list_issues()
    print(f"loaded {digest.returned} issues")


if __name__ == "__main__":
    main()
