# ADR 0003: Share A Core Library Across Interfaces

## Context

Both the CLI and API need to list issues, apply filters, and fetch individual items. Duplicating that logic would make the repo noisier and weaken the learning value.

## Decision

Keep domain models, errors, protocols, configuration, and issue digest behavior in `packages/core`, then have `cli` and `api` depend on it.

## Consequences

- The CLI and API stay thin and focused on transport concerns.
- Tests can target the reusable logic directly.
- Future integrations can reuse the same service boundary.
- The repo demonstrates composition and packaging reuse without reaching for a framework.
