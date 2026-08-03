# CORE-022 Runtime API Gap Analysis

## Canonical References

- CANON-058 §51 Platform APIs
- CANON-059 CORE-022 Runtime API Platform
- CANON-061 Identity & Authentication
- CANON-064 Cloud APIs
- CANON-066 Implementation Package Workflow

---

## Repository Status

Current Runtime HTTP Server exposes:

- /health
- /ready
- /status
- /metrics
- /webhook/github
- /webhook/telegram

Current implementation is deterministic and communicates through Runtime handlers.

Bootstrap wiring already exists.

---

## Canonical Compliance

Verified:

- CLI interface
- Telegram Runtime Interface
- GitHub Webhooks
- Internal Runtime HTTP interface
- Event Bus communication

Verified PASS.

---

## Missing Canonical Specification

The canonical documents define that Runtime APIs shall exist.

However they do NOT define:

- REST endpoint list
- request schemas
- response schemas
- authentication flow
- versioning contract
- OpenAPI specification
- HTTP status contract

Therefore these interfaces cannot be implemented canonically.

---

## Required Future Canonical Work

Before extending Runtime HTTP Server, create a new canonical specification describing:

- Runtime REST API
- endpoint catalogue
- JSON contracts
- authentication
- authorization
- versioning
- API lifecycle
- OpenAPI definition

Only after approval should Runtime HTTP endpoints be expanded.

---

## Conclusion

CORE-022 implementation SHALL NOT invent public REST endpoints.

Current implementation remains compliant with CANON-058 and CANON-059.

Future Runtime REST API requires a dedicated canonical specification before implementation.
