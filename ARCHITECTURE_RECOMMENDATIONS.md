# Project Architecture Recommendations — Backend Experience

Purpose: a concise, actionable audit and roadmap for splitting large modules, fixing typos, improving docs, and prioritizing backend optimizations.

---

## 1. Summary

This document lists files that currently do too many things and should be split, exact suggestions for splits, discovered typos and how to fix them, missing architecture pieces, docstring guidance, and recommended optimizations.

## 2. Files to split (high priority)

- `app/app.py` — if this contains both app creation and many route registrations or config: split into
  - `app/main.py` (create FastAPI app and startup/shutdown hooks)
  - `app/config.py` (env, settings, constants)
  - `app/routes/__init__.py` (import routers)

- `core/ai_driver.py` — often mixes HTTP/AI-client initialization and higher-level orchestration. Split into:
  - `core/ai_client.py` (thin wrapper around the external API/client)
  - `core/ai_service.py` (business logic that calls `ai_client` and processes results)

- `core/mcp_registry.py` — split responsibilities: registry storage vs adapters vs execution logic.
  - `core/registry.py` (registry data structures, register/unregister, list)
  - `core/registry_executor.py` (validation, execution orchestration)
  - `core/adapters/` (adapter implementations for different tool types)

- `core/file_utils.py` — if it includes scanning, parsing, and upload logic:
  - `core/fs_walker.py` (filesystem traversal and scanning)
  - `core/file_parser.py` (metadata extraction, mime detection)
  - `core/file_helpers.py` (path helpers, normalization)

- `services/file_service.py` — separate ingestion from query/update logic:
  - `services/ingest_service.py` (ingest pipelines and batching)
  - `services/file_store.py` (CRUD operations and DB mapping)

- `routes/*_router.py` — keep routers thin (only request validation and response), move business logic to `services/`.

## 3. Why split (short rationale)

- Single Responsibility: smaller files are easier to test, reason about, and change.
- Faster reviews: reviewers focus on one concern per file.
- Reuse & DI: separated clients/adapters are easier to mock or swap.

## 4. Concrete typos and fixes (examples found)

- In `services/db_service.py`:
  - "Retrived" → "Retrieved"
  - "retrived" → "retrieved"
  - "Retrueving" → "Retrieving" (or "Retrieving")
  - "targest_path" → "target_path"
  - "direcrt" → "direct"

  Fix: run a repo-wide replace for these tokens and run tests/linters afterwards.

- In `PROJECT_FLOW.md` there were legacy typos before your earlier fix, watch for `FileServie`, `Retrive`, `CLient`, `roter`, `respone` — normalize to `FileService`, `Retrieve`, `Client`, `router`, `response`.

## 5. Missing or weak architecture pieces (and where to place them)

- README and CONTRIBUTING (root): short project overview, how to run locally, test instructions, and lint/format rules.
- `pyproject.toml` / `requirements.txt`: explicit pinned dependencies and minimum Python version.
- Tests (`tests/`): unit tests for `core/mcp_registry.py`, `services/file_service.py`, `core/ai_driver.py`.
- Migrations (`alembic/`): DB schema migrations if using SQLAlchemy.
- Health & metrics (`app/monitoring.py`): simple `/health` and metrics hooks.
- CI (`.github/workflows/ci.yml`): run lint, format, unit tests, type-checks.
- Logging policy: central `logging_config.py` (already present) — enforce structured logs across modules.

## 6. Docstring and documentation guidance

- Module-level docstring at top of each `.py` explaining purpose in 1-2 lines.
- Public classes: class docstring describing responsibility and main public methods.
- Public functions: short summary line, `Args:`, `Returns:`, and `Raises:` sections using Google style or NumPy style. Example:

```python
def ingest_file(db: Session, path: str) -> File:
    """Create a `File` record from `path` and save to DB.

    Args:
        db: Active SQLAlchemy session.
        path: Absolute path to the file on disk.

    Returns:
        The saved `File` ORM instance.

    Raises:
        FileNotFoundError: If `path` does not exist.
    """
    ...
```

- Where to write docstrings: every module, every public class, and every function that is more than trivial (more than 3 lines).
- Add `docs/` folder with short architecture.md that references this file and includes a simple system diagram.

## 7. Optimizations & tech debt (practical priorities)

1. DB: Add indexes on `File.user_id`, `File.parent_path`, and any frequently filtered columns; review slow queries and add pagination.
2. Scanning/ingest: Make the scanner batch writes and run ingestion in background workers (Celery / RQ / asyncio tasks).
3. Caching: Cache `mcp_registry.get_tools()` result for a short TTL to avoid repeated lookups on frequent queries.
4. Registry execution: enforce timeouts and sandboxing for executed tools; run calls with cancellation/timeout.
5. Concurrency: use async endpoints for IO-bound operations (file reads, external API calls) and ensure DB sessions are used correctly in async contexts.
6. Telemetry: Add success/failure counters for tool executions and ingestion; log durations for long-running operations.
7. Type safety: add type hints, run `mypy` and fix type errors gradually.
8. Static analysis: add `ruff/flake8` and enforce formatting via `black`.

## 8. Quick implementation plan (first 5 steps)

1. Add `ARCHITECTURE_RECOMMENDATIONS.md` (this file). — done.
2. Run a focused search/replace for the confirmed typos and fix them.
3. Create `README.md` with local setup and run steps.
4. Split one large file as a proof-of-concept (suggest `core/mcp_registry.py` into `core/registry.py` + `core/registry_executor.py`).
5. Add unit tests for `core/registry.py` and add CI workflow.

## 9. Notes on review and next steps

- I can implement the quick wins: fix typos in `services/db_service.py`, add `README.md`, and scaffold a unit test for `core/mcp_registry.py`. Tell me which of these you want first and I'll apply the changes.

---

End of document.
