# Development notes — Library API

## Summary
Short retrospective documenting major challenges, solutions, possible improvements, and lessons learned while implementing the Library API.

## Challenges faced
- Circular imports and NameError for models (e.g. User, Book, Author, BorrowRecord) caused by top-level imports between routers, security, and models.
- FastAPI dependency analysis triggering imports at module load time (exposed import-order issues).
- SQLAlchemy mapping issues (missing/mis-declared mapped_column for some fields).
- Password hashing backend compatibility in test env (bcrypt wheel/platform issues).
- FastAPI form parsing raising errors when `python-multipart` was missing.
- Tests using the real DB file (stateful tests) instead of isolated in-memory DB.
- Time constraints to add migrations, CI, and comprehensive tests.

## How issues were solved
- Made imports lazy where appropriate (import models inside functions like get_current_user) to break circular dependencies.
- Adjusted security module to use OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login") and implemented a get_current_user dependency that imports models at runtime.
- Fixed SQLAlchemy column declarations (e.g. added mapped_column for due_date) so models are mapped correctly.
- Switched to a pure-Python hashing scheme for tests (sha256_crypt) to avoid bcrypt binary issues; noted to restore bcrypt for production.
- Added `python-multipart` to requirements and installed it so FastAPI's OAuth2 form parsing works.
- Added a smoke unittest (tests/test_smoke.py) and a Postman collection for manual verification.
- Kept changes minimal and targeted to make the app importable and testable quickly.

## What would be done differently with more time
- Introduce Alembic migrations and a proper schema migration workflow.
- Add unit + integration tests using pytest with fixtures and an in-memory SQLite DB for isolation.
- Implement a clear service layer to decouple business logic from routers and simplify testing.
- Re-enable bcrypt (or argon2) in production and ensure wheels are available in CI.
- Add CI pipeline (GitHub Actions) to run linting, type checks (mypy), tests, and build steps.
- Add Dockerfile and docker-compose for reproducible local/dev environments.
- Add more robust validation, rate limiting, and role-based access control for endpoints.
- Improve API pagination, sorting, and filtering options and document them in OpenAPI.

## Lessons learned
- FastAPI's dependency inspection can surface subtle import-order problems; avoid importing models at module scope in shared utility modules.
- Lazy imports and clear dependency injection boundaries reduce circular-import risk.
- Tests should run against isolated databases to avoid flaky behavior; defaulting to file-based SQLite is convenient but not ideal for automated tests.
- Third-party native dependencies (bcrypt) can block test portability — choose test-friendly defaults or ensure CI installs wheels.
- Small smoke tests + a Postman collection are invaluable for fast manual verification during development.