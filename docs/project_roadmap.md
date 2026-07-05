# Project Roadmap - Natural Language File Management System

## Overview

This project is an AI-powered file management system featuring intelligent file analysis, automation, and user-driven file operations. The roadmap guides the project's evolution from a functional prototype into a robust, scalable, and production-ready platform.

---

## 📈 Project Maturity & Status

### 1. 🟢 Beginner & Intermediate Levels (100% Completed)
- [x] Basic file and folder listing.
- [x] Database-backed persistence for users, files, and tasks.
- [x] Core analysis features:
  - [x] Total file & folder count.
  - [x] Largest file & largest folder detection.
  - [x] Folder size calculation.
  - [x] File type distribution reporting.
  - [x] Empty folder detection.
- [x] Duplicate file detection (grouped securely by SHA-256 content hashes per user context).
- [x] Automatic sorting workflows (physically moves files into folders and synchronizes DB metadata).

### 2. 🟡 Advanced Level (In Progress)
- [x] Natural language interaction (bridges user queries to tools).
- [x] AI-driven tool selection & execution (Gemini-2.5-flash with structured JSON output).
- [x] Multi-step workflows & execution orchestration.
- [x] Code Quality, Testing & Repository Polish:
  - [x] Manually curated dependencies (`requirements.txt`).
  - [x] Environment configuration template (`.env.example`).
  - [x] Open-source licensing (MIT License).
  - [x] Professional `.gitignore` covering caching, logs, IDEs, and local test scans.
  - [x] Clean repository structure with all documentation in the `docs/` folder.
  - [x] Automated unit test coverage for database service routines and filesystem helpers using an in-memory SQLite DB.
- [ ] Background/asynchronous task processing (celery or rq integration).
- [ ] Safe execution mechanisms (confirmations/dry-runs for destructive deletes or movements).

---

## 🗺️ Detailed Roadmap

### Phase 1 - Foundation & Stability (Completed)
- [x] Secure duplicate file query logic to avoid cross-user data leaks.
- [x] Implement database updates to synchronize physical file movement with database records.
- [x] Fix global state reports in file-sorting helpers.
- [x] Clean up type hints (e.g. `get_newest_file` returning `File` instead of `str`).
- [x] Standardize folder metadata scanning on startup.

### Phase 2 - Release Packaging (Completed)
- [x] Create a comprehensive `README.md` with conceptual diagrams and badges.
- [x] Copy and link visual CLI execution and sorting results screenshots inside the readme.
- [x] Curate minimal requirements and `.env.example` configurations.
- [x] Setup unit tests in `tests/test_file_utils.py` and `tests/test_db_service.py`.

### Phase 3 - Next Generation Advanced Goals (Backlog)
- [ ] **Dynamic Folder Scanning:** Allow the AI to scan and index any directory on command rather than a single configured startup folder.
- [ ] **Async Ingestion & Sorting:** Offload heavy indexing and physical sorting actions to background workers.
- [ ] **Alembic Database Migrations:** Establish SQLAlchemy schema version tracking.
- [ ] **Dockerization:** Build a `docker-compose.yml` defining PostgreSQL and FastAPI backend services.
- [ ] **API documentation:** Build full REST swagger documentation for external developers.
