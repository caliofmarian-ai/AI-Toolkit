"""
CORE-021 — Runtime Configuration Manager
CANON-055 §5, CANON-056 §11

Loads, validates and exposes Runtime configuration from environment
variables and optional configuration files.
"""

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RuntimeConfig:
    """Validated Runtime configuration."""

    # Runtime mode
    runtime_mode: str = "NORMAL"

    # HTTP server settings (health/readiness/webhooks)
    http_host: str = "0.0.0.0"
    http_port: int = 8080

    # Environment
    environment: str = "production"

    # GitHub integration
    github_webhook_secret: str = ""
    github_token: str = ""

    # Telegram integration
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    # Scheduler
    scheduler_interval_seconds: int = 60

    # Runtime loop
    runtime_loop_interval_seconds: int = 30

    # Persistence
    state_dir: str = ".ai/runtime/state"
    logs_dir: str = ".ai/runtime/logs"
    checkpoints_dir: str = ".ai/runtime/checkpoints"
    sessions_dir: str = ".ai/runtime/sessions"
    cache_dir: str = ".ai/runtime/cache"

    # Recovery
    max_recovery_attempts: int = 3

    @classmethod
    def from_environment(cls) -> "RuntimeConfig":
        """Load configuration from environment variables."""
        return cls(
            runtime_mode=os.environ.get("RUNTIME_MODE", "NORMAL").upper(),
            http_host=os.environ.get("RUNTIME_HTTP_HOST", "0.0.0.0"),
            http_port=int(os.environ.get("PORT", os.environ.get("RUNTIME_HTTP_PORT", "8080"))),
            environment=os.environ.get("RAILWAY_ENVIRONMENT", os.environ.get("ENVIRONMENT", "production")),
            github_webhook_secret=os.environ.get("GITHUB_WEBHOOK_SECRET", ""),
            github_token=os.environ.get("GITHUB_TOKEN", ""),
            telegram_bot_token=os.environ.get("TELEGRAM_BOT_TOKEN", ""),
            telegram_chat_id=os.environ.get("TELEGRAM_CHAT_ID", ""),
            scheduler_interval_seconds=int(os.environ.get("SCHEDULER_INTERVAL_SECONDS", "60")),
            runtime_loop_interval_seconds=int(os.environ.get("RUNTIME_LOOP_INTERVAL_SECONDS", "30")),
            state_dir=os.environ.get("RUNTIME_STATE_DIR", ".ai/runtime/state"),
            logs_dir=os.environ.get("RUNTIME_LOGS_DIR", ".ai/runtime/logs"),
            checkpoints_dir=os.environ.get("RUNTIME_CHECKPOINTS_DIR", ".ai/runtime/checkpoints"),
            sessions_dir=os.environ.get("RUNTIME_SESSIONS_DIR", ".ai/runtime/sessions"),
            cache_dir=os.environ.get("RUNTIME_CACHE_DIR", ".ai/runtime/cache"),
            max_recovery_attempts=int(os.environ.get("MAX_RECOVERY_ATTEMPTS", "3")),
        )

    def validate(self) -> list:
        """Return a list of validation errors (empty = valid)."""
        errors = []
        valid_modes = {"NORMAL", "SIMULATION", "VALIDATION", "MAINTENANCE", "RECOVERY", "SHUTDOWN"}
        if self.runtime_mode not in valid_modes:
            errors.append(f"Invalid RUNTIME_MODE: {self.runtime_mode}. Must be one of {valid_modes}")
        if self.http_port < 1 or self.http_port > 65535:
            errors.append(f"Invalid HTTP port: {self.http_port}")
        return errors

    def to_dict(self) -> dict:
        return {
            "runtime_mode": self.runtime_mode,
            "http_host": self.http_host,
            "http_port": self.http_port,
            "environment": self.environment,
            "scheduler_interval_seconds": self.scheduler_interval_seconds,
            "runtime_loop_interval_seconds": self.runtime_loop_interval_seconds,
            "state_dir": self.state_dir,
            "max_recovery_attempts": self.max_recovery_attempts,
        }
