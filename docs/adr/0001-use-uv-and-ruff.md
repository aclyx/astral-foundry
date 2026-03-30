# ADR 0001: Use uv And Ruff

## Context

The workspace needs a small set of tools that are fast, consistent, and easy to apply every day. The goal is learning modern Python workflow, not maintaining a fragmented toolchain.

## Decision

Use `uv` for Python installation, dependency management, locking, syncing, and command execution. Use `ruff` for both linting and formatting.

## Consequences

- New contributors learn one default command flow instead of several competing ones.
- The repo gets a single lockfile and a fast install path.
- Formatting and linting stay aligned because the same tool family owns both concerns.
- We avoid a common Python failure mode where tool sprawl becomes part of the learning burden.
