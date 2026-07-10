"""The 10-category, ~12-item-each quality checklist used to build the review prompt
and to normalize the LLM's findings into a 0-100 score."""

QUALITY_CHECKLIST: dict[str, list[str]] = {
    "Maintainability": [
        "Functions are under ~50 lines",
        "Classes are under ~200 lines",
        "Each unit follows the single responsibility principle",
        "No significant DRY violations (duplicated logic)",
        "Non-obvious logic has explanatory comments",
        "Complex conditionals/algorithms are documented",
    ],
    "Readability": [
        "Variable names are descriptive",
        "Function names clearly state intent",
        "Code is consistently indented/formatted",
        "Lines are under ~120 characters",
        "Type hints are present (Python) / types declared (TypeScript)",
        "Public functions/classes have docstrings",
    ],
    "Modularity": [
        "Clear separation of concerns between layers",
        "Components/functions are reusable",
        "Low coupling between modules",
        "High cohesion within modules",
        "No circular dependencies",
        "Clear interfaces/contracts between layers",
    ],
    "Coding Standards": [
        "PEP 8 compliance (Python)",
        "ESLint-style compliance (TypeScript/React)",
        "Consistent naming conventions",
        "No hardcoded configuration values",
        "Configuration externalized (env vars/settings)",
    ],
    "Exception Handling": [
        "Try/except blocks around I/O and network calls",
        "Specific exception types caught, not bare except",
        "Error messages are informative",
        "Graceful fallbacks implemented where appropriate",
        "Errors are logged",
        "No silent failures (swallowed exceptions)",
    ],
    "Security": [
        "No hardcoded secrets or API keys",
        "Input validation present at system boundaries",
        "SQL injection prevented (parameterized queries only)",
        "XSS prevention on frontend (no unsanitized HTML injection)",
        "Authentication/authorization checks on protected routes",
        "No sensitive data logged",
    ],
    "Database Access": [
        "Parameterized queries / ORM used exclusively",
        "Connections/sessions properly scoped and closed",
        "Transactions used appropriately for multi-step writes",
        "Foreign keys are indexed",
        "No obvious N+1 query patterns",
    ],
    "Test Readiness": [
        "Code is testable (dependencies injectable, not hardwired)",
        "External services (LLM, DB) can be mocked",
        "Pure functions separated from side-effecting ones",
        "Edge cases are structurally reachable for testing",
    ],
    "Configuration Handling": [
        "All secrets/config loaded from environment variables",
        "Sensible defaults provided for non-secret config",
        "No environment-specific values hardcoded in source",
    ],
    "Traceability": [
        "Code references the requirement/spec it implements (docstring or comment)",
        "Function/module names align with the traceability matrix",
        "Audit logging present for mutating actions",
    ],
}

SEVERITY_LEVELS = ["CRITICAL", "MAJOR", "MINOR", "INFO"]

POINTS_PER_ITEM = {"pass": 2, "warning": 1, "fail": 0}
