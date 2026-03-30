# Learning Path

This path is meant to be worked through by changing the repo, not just reading it. Each milestone is intentionally scoped so you can make a real change, run the checks, and build intuition from the feedback loop.

## Milestone 1: Workspace And Tooling Fluency

Goals

- Understand the virtual root workspace and why the real code lives in package members
- Use `uv` for Python installation, syncing, locking, and running commands
- Use `ruff` and `pytest` as the everyday feedback loop

What to read in the codebase

- `pyproject.toml`
- `.python-version`
- `scripts/bootstrap.sh`
- `scripts/check.sh`
- `.github/workflows/ci.yml`

What to modify

- Change the line length in Ruff and re-run formatting
- Add one dev dependency to `pyproject.toml`, then refresh the lockfile

Suggested exercises

- Run `uv lock` after changing a dependency range and inspect the lockfile diff
- Add a new root script in `scripts/` that runs only the core package tests

What to notice if you come from TypeScript

- The workspace root behaves more like a package manager root than a runtime root
- Python packaging is explicit and installation-driven; importability comes from the environment, not path aliases
- `uv run` replaces a lot of what would otherwise be `npx`, `pnpm exec`, or a custom shell wrapper

## Milestone 2: Typed Core Library

Goals

- Get comfortable with dataclasses, `StrEnum`, and simple immutable domain objects
- See how `Protocol` creates an abstraction boundary without inheritance
- Keep business logic pure and local

What to read in the codebase

- `packages/core/src/core/models.py`
- `packages/core/src/core/protocols.py`
- `packages/core/src/core/services.py`
- `packages/core/src/core/errors.py`
- `packages/core/tests/test_services.py`

What to modify

- Add label filtering to `DigestRequest` and `IssueDigestService`
- Add one more explicit domain error case if a request shape becomes invalid

Suggested exercises

- Add a `priority` field to `Issue` and sort by it before `updated_at`
- Add a new status value and update tests to prove the behavior stays coherent

What to notice if you come from TypeScript

- Python type hints are valuable, but the runtime model stays simple unless you choose otherwise
- A `Protocol` is closer to a structural TypeScript interface than a classic OO base class
- Dataclasses are often enough where a TS habit might push you toward a class hierarchy

## Milestone 3: CLI Application

Goals

- Practice CLI structure with `argparse` instead of reaching for a framework too early
- Separate parsing, config, output, and command behavior
- Handle errors explicitly and keep user-facing messages readable

What to read in the codebase

- `packages/cli/src/cli_app/main.py`
- `packages/cli/src/cli_app/config.py`
- `packages/cli/src/cli_app/output.py`
- `packages/cli/src/cli_app/commands/items.py`
- `packages/cli/tests/test_main.py`

What to modify

- Add a new CLI subcommand under `items`
- Teach the text renderer to show one more field without making output noisy

Suggested exercises

- Add `items export --path <file>` and write JSON to disk
- Add `--assignee` support to the remote `fetch` path once the API exposes it

What to notice if you come from TypeScript

- Standard-library CLI tooling goes further than many TS engineers expect
- TOML parsing is in the standard library on modern Python, so small config files do not need extra packages
- Dependency injection often becomes plain function parameters instead of framework-managed objects

## Milestone 4: FastAPI Service

Goals

- Expose the same core behavior over HTTP without moving business logic into the route layer
- Use Pydantic for transport schemas while keeping domain models in `core`
- Keep dependency wiring thin and obvious

What to read in the codebase

- `packages/api/src/api/main.py`
- `packages/api/src/api/deps.py`
- `packages/api/src/api/routers/items.py`
- `packages/api/src/api/services/items.py`
- `packages/api/tests/test_items.py`

What to modify

- Add pagination parameters and response metadata
- Add one more endpoint that reuses the same core service

Suggested exercises

- Add `/items/{item_id}/summary`
- Split list and detail schemas if the transport needs different shapes

What to notice if you come from TypeScript

- FastAPI dependency wiring is already enough for most small-to-medium services
- Pydantic models are transport objects here, not replacements for every domain object
- The route layer should stay thin; the core service remains the source of truth

## Milestone 5: Async I/O And External Integrations

Goals

- Learn where async genuinely helps and where sync code is simpler
- Use `httpx` for both sync and async integration points
- Start replacing in-memory boundaries with real I/O

What to read in the codebase

- `examples/async_script.py`
- `packages/cli/src/cli_app/commands/fetch.py`
- `packages/core/src/core/protocols.py`

What to modify

- Replace the in-memory source with a small HTTP-backed implementation
- Add explicit timeout handling and map transport failures into domain errors

Suggested exercises

- Create a new source that reads issues from a local JSON file
- Add retry or backoff behavior behind a separate adapter instead of inside the service

What to notice if you come from TypeScript

- Python async is for I/O boundaries, not a default posture for all code
- It is normal to keep the domain service synchronous and push async to the edge
- `httpx` gives you sync and async clients with very similar APIs, which makes comparison easier

## Milestone 6: Production Discipline

Goals

- Tighten the repo without turning it into ceremony-heavy enterprise code
- Use tests, coverage, linting, and CI as maintenance tools instead of afterthoughts
- Learn where to add guardrails and where to keep the code small

What to read in the codebase

- `.github/workflows/ci.yml`
- `scripts/check.sh`
- `docs/architecture.md`
- `docs/adr/`

What to modify

- Raise the coverage standard once you are comfortable with the shape of the repo
- Add one more CI step only if it earns its keep

Suggested exercises

- Add type checking with a tool you actually plan to keep using
- Add a release or package build check after you have a reason to publish artifacts

What to notice if you come from TypeScript

- Python teams often get the most leverage from a few sharp tools used consistently
- Over-abstracting early feels just as expensive in Python as it does in TS
- Small, explicit modules usually age better than broad frameworks or shared base classes
