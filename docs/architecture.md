# Architecture

## Why Split The Repo Into `core`, `cli`, And `api`

The repo is split by responsibility, not by technology fashion.

- `core` owns business logic and typed domain objects.
- `cli` owns command-line parsing, user-facing rendering, local config, and HTTP client integrations.
- `api` owns transport concerns: FastAPI routing, Pydantic schemas, and dependency wiring.

This gives you a clean place to practice Python packaging and reuse without drifting into enterprise layering. If you come from TypeScript, the goal is similar to keeping domain code separate from React, Nest, or script entrypoints, but with a stronger emphasis on installed packages and import boundaries.

## Where Business Logic Lives

Business logic lives in `packages/core/src/core/services.py`.

That service accepts an `IssueSource` protocol instead of importing a concrete repository implementation. The source boundary is structural, so any object with `list_issues()` can satisfy it. The in-memory source is intentionally simple because the learning value is in the seam: you can swap in a file-backed, HTTP-backed, or test double implementation without rewriting the service.

The CLI and API should stay thin. They translate user or HTTP input into a `DigestRequest`, call the core service, and render or serialize the result.

## Dependency Flow

Dependency flow is one-directional:

- root workspace -> `cli`, `api`, tooling
- `cli` -> `core`
- `api` -> `core`
- `core` -> no internal package dependencies

There is no path where `core` imports from `cli` or `api`, and there is no duplicated filtering logic in the interface layers.

## Pragmatic Typing

Typing is used where it clarifies contracts:

- `dataclass` and `StrEnum` for domain objects
- `Protocol` for source boundaries
- Pydantic models for HTTP transport schemas
- annotations on public functions and important internals

Typing is not used as an excuse to introduce unreadable type machinery. The repo is intentionally tuned for an engineer who values correctness but still wants the code to read like Python instead of a type puzzle.

## Intentionally Excluded

This repo does not include:

- a database or ORM
- a dependency injection framework
- a background worker system
- a plugin architecture
- Docker Compose or local infrastructure orchestration
- microservice choreography

Those are all real tools, but they are not the right starting point for building fluency in modern Python fundamentals.
