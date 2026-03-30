# ADR 0002: Use A Workspace Structure

## Context

The repo needs multiple interfaces over the same domain logic, and part of the learning goal is understanding modern Python packaging in a multi-package setup.

## Decision

Use a virtual workspace root with explicit package members under `packages/`.

## Consequences

- The root can centralize tooling, shared config, and daily workflow.
- Each package keeps a clear responsibility and its own metadata.
- The repo teaches installed-package boundaries instead of ad hoc relative imports.
- The structure stays small enough to understand without bringing in monorepo tooling complexity.
