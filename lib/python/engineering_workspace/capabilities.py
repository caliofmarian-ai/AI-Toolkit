"""
CANON-081 Engineering Workspace

CORE-022 Engineering Workspace Kernel

Canonical Capability Definitions
"""

from __future__ import annotations

from enum import Enum


class Capability(str, Enum):
    #
    # Repository
    #
    READ_REPOSITORY = "repository.read"
    WRITE_REPOSITORY = "repository.write"
    INSPECT_REPOSITORY = "repository.inspect"

    #
    # Filesystem
    #
    READ_FILES = "filesystem.read"
    WRITE_FILES = "filesystem.write"
    CREATE_FILES = "filesystem.create"
    DELETE_FILES = "filesystem.delete"

    #
    # Git
    #
    GIT_STATUS = "git.status"
    GIT_DIFF = "git.diff"
    GIT_ADD = "git.add"
    GIT_COMMIT = "git.commit"
    GIT_PULL = "git.pull"
    GIT_PUSH = "git.push"

    #
    # GitHub
    #
    GITHUB_READ = "github.read"
    GITHUB_ISSUES = "github.issues"
    GITHUB_PULL_REQUESTS = "github.pull_requests"
    GITHUB_ACTIONS = "github.actions"

    #
    # Railway
    #
    RAILWAY_READ = "railway.read"
    RAILWAY_DEPLOY = "railway.deploy"
    RAILWAY_LOGS = "railway.logs"

    #
    # Runtime
    #
    RUNTIME_READ = "runtime.read"
    RUNTIME_CONTROL = "runtime.control"

    #
    # Knowledge
    #
    KNOWLEDGE_READ = "knowledge.read"
    KNOWLEDGE_UPDATE = "knowledge.update"

    #
    # Canonical
    #
    CANONICAL_READ = "canonical.read"
    CANONICAL_VALIDATE = "canonical.validate"
    CANONICAL_MATERIALIZE = "canonical.materialize"

    #
    # AI
    #
    AI_CHAT = "ai.chat"
    AI_ANALYZE = "ai.analyze"
    AI_PLAN = "ai.plan"
    AI_EXECUTE = "ai.execute"

    #
    # Testing
    #
    RUN_TESTS = "testing.run"

    #
    # Terminal
    #
    TERMINAL_EXECUTE = "terminal.execute"


ALL_CAPABILITIES = tuple(Capability)
