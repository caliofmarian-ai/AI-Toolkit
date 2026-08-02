# System Invariants
Version: 1.0.0
Status: CANONICAL
Authority: OWNER

# PURPOSE

This document defines the immutable rules of AI Toolkit.

These invariants shall never be violated by any engine, plugin, workflow or future version unless a new major version explicitly replaces this document.

---

# CORE PRINCIPLE

Architecture is authoritative.

Implementation follows architecture.

Documentation precedes implementation.

---

# CLI INVARIANTS

The CLI is the only supported public interface.

Every public command must remain backward compatible throughout version 1.x.

Breaking CLI changes require a new major version.

---

# ENGINE INVARIANTS

Every engine shall implement the Engine Interface Specification.

Every engine shall expose one public entry point.

Every engine shall be independently executable.

Every engine shall be replaceable without modifying other engines.

---

# STATE INVARIANTS

The .ai directory is the only workspace owned by AI Toolkit.

Project source files are never used as runtime storage.

Execution state must always be recoverable.

Resume must always reconstruct the latest execution state.

---

# LOGGING INVARIANTS

Every engine shall generate logs.

Every failure shall be logged.

Every execution shall be timestamped.

Logs shall never silently disappear.

---

# MEMORY INVARIANTS

Context is persistent.

Execution history is persistent.

Repository knowledge is persistent.

Owner decisions are persistent.

Memory shall survive application restarts.

---

# GIT INVARIANTS

Repository integrity is mandatory.

Working tree shall be verified before execution.

Commits shall never occur silently.

Every automated commit shall contain a meaningful message.

---

# GITHUB INVARIANTS

Issues are authoritative.

Pull Requests represent completed work.

Releases represent stable milestones.

No workflow shall bypass GitHub history.

---

# TESTING INVARIANTS

Every engine must be testable.

Every public command must have at least one integration test.

Every regression must become a permanent automated test.

---

# WORKFLOW INVARIANTS

Inspect always precedes planning.

Planning always precedes execution.

Execution always precedes review.

Review always precedes release.

Release always follows successful validation.

---

# OBSERVABILITY INVARIANTS

Every workflow shall expose progress.

Every workflow shall expose current stage.

Every workflow shall expose execution status.

No hidden execution is permitted.

---

# PLUGIN INVARIANTS

Plugins extend the platform.

Plugins never modify the platform core.

Plugins communicate only through public interfaces.

Plugins may be disabled without affecting the core.

---

# SECURITY INVARIANTS

User data shall never be modified without explicit workflow execution.

Repository history shall never be rewritten automatically.

Credentials shall never be stored in logs.

Secrets shall remain external to the toolkit.

---

# VERSIONING INVARIANTS

Major versions may introduce breaking changes.

Minor versions remain backward compatible.

Patch versions contain only fixes.

Canonical documents define platform behavior.

---

# FUTURE INVARIANTS

Every future engine shall comply with these invariants before implementation.

Architecture remains the single source of truth.

