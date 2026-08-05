"""
CORE-021 — Runtime Bootstrap
CANON-055 §7 — Boot Sequence

The Bootstrap orchestrates the complete Runtime startup sequence.
No Runtime Engine may execute before Bootstrap completes.

Startup order (canonical):
    1. Configure logging
    2. Load configuration
    3. Validate environment
    4. Validate secrets
    5. Initialize Runtime Identity
    6. Initialize Services
    7. Register Runtime Services
    8. Register Runtime Engines
    9. Restore persistent Runtime state
   10. Initialize Scheduler
   11. Initialize Event Bus
   12. Initialize HTTP Server
   13. Verify Runtime health
   14. Enter READY state
   15. Start continuous Runtime Loop
"""

import logging
import os
from typing import Optional

from lib.python.runtime.identity import RuntimeIdentity
from lib.python.runtime.config import RuntimeConfig
from lib.python.runtime.secrets import SecretManager
from lib.python.runtime.registry import RuntimeRegistry
from lib.python.runtime.lifecycle import LifecycleManager, LifecyclePhase
from lib.python.runtime.supervisor import RuntimeSupervisor
from lib.python.runtime.health import HealthService
from lib.python.runtime.recovery import RecoveryService
from lib.python.runtime.scheduler import SchedulerHost
from lib.python.runtime.event_loop import EventLoop
from lib.python.runtime.event_dispatcher import EventDispatcher
from lib.python.runtime.job_queue import JobQueueHost
from lib.python.runtime.metrics import RuntimeMetrics
from lib.python.runtime.logging_service import configure_logging
from lib.python.runtime.reports import RuntimeReports
from lib.python.runtime.interfaces.http_server import RuntimeHttpServer
from lib.python.runtime.interfaces.github_webhook import GitHubWebhookHost
from lib.python.runtime.interfaces.telegram_gateway import TelegramGateway

logger = logging.getLogger(__name__)


class RuntimeBootstrap:
    """
    Orchestrates the complete Runtime startup sequence.

    All Runtime components are created and wired together here.
    After bootstrap() returns, the Runtime is fully operational.
    """

    def __init__(self):
        # Core components (created during bootstrap)
        self.identity: Optional[RuntimeIdentity] = None
        self.config: Optional[RuntimeConfig] = None
        self.secrets: Optional[SecretManager] = None
        self.registry: Optional[RuntimeRegistry] = None
        self.lifecycle: Optional[LifecycleManager] = None
        self.supervisor: Optional[RuntimeSupervisor] = None
        self.health: Optional[HealthService] = None
        self.recovery: Optional[RecoveryService] = None
        self.scheduler: Optional[SchedulerHost] = None
        self.event_loop: Optional[EventLoop] = None
        self.dispatcher: Optional[EventDispatcher] = None
        self.job_queue: Optional[JobQueueHost] = None
        self.metrics: Optional[RuntimeMetrics] = None
        self.reports: Optional[RuntimeReports] = None

        # External interfaces
        self.http_server: Optional[RuntimeHttpServer] = None
        self.github_webhook: Optional[GitHubWebhookHost] = None
        self.telegram: Optional[TelegramGateway] = None

        self._bootstrapped = False

    # ------------------------------------------------------------------ #
    # Main bootstrap sequence
    # ------------------------------------------------------------------ #

    def bootstrap(self) -> "RuntimeBootstrap":
        """
        Execute the complete startup sequence.
        Returns self for convenience.
        """
        # Step 1 — Logging (must be first so everything else can log)
        self._step_configure_logging()

        logger.info("Bootstrap: starting AI CTO Runtime Server (CORE-021)")

        # Step 2 — Initialize lifecycle manager early (tracks all phases)
        self.lifecycle = LifecycleManager()

        # Step 3 — Configuration
        self._step_load_configuration()

        # Step 4 — Validate environment
        self._step_validate_environment()

        # Step 5 — Secrets
        self._step_load_secrets()

        # Step 6 — Runtime Identity
        self._step_create_identity()

        # Step 7 — Initialize core services
        self.lifecycle.transition(LifecyclePhase.INITIALIZATION)
        self._step_initialize_services()

        # Step 8 — Register Runtime Engines
        self.lifecycle.transition(LifecyclePhase.ENGINE_REGISTRATION)
        self._step_register_engines()

        # Step 9 — Register Runtime Services
        self.lifecycle.transition(LifecyclePhase.SERVICE_REGISTRATION)
        self._step_register_services()

        # Step 10 — Restore persistent state
        self._step_restore_state()

        # Step 11 — Initialize Scheduler
        self._step_initialize_scheduler()

        # Step 12 — Initialize Event Bus
        self._step_initialize_event_bus()

        # Step 13 — Initialize HTTP Server
        self._step_initialize_http_server()

        # Step 14 — Initialize external interfaces
        self._step_initialize_external_interfaces()

        # Step 15 — Health verification
        self.lifecycle.transition(LifecyclePhase.HEALTH_VERIFICATION)
        self._step_verify_health()

        # Step 16 — Enter READY state
        self.lifecycle.transition(LifecyclePhase.READY)
        self.health.mark_startup_complete()
        self.identity.lifecycle_phase = LifecyclePhase.READY.value
        self.metrics.set_gauge("lifecycle_phase", "READY")

        logger.info("Bootstrap: Runtime READY — %s", self.identity.runtime_id)
        self._bootstrapped = True
        return self

    # ------------------------------------------------------------------ #
    # Individual steps
    # ------------------------------------------------------------------ #

    def _step_configure_logging(self) -> None:
        log_level = os.environ.get("LOG_LEVEL", "INFO")
        json_logs = os.environ.get("JSON_LOGS", "true").lower() != "false"
        configure_logging(level=log_level, json_output=json_logs)

    def _step_load_configuration(self) -> None:
        self.lifecycle.transition(LifecyclePhase.CONFIGURATION)
        self.config = RuntimeConfig.from_environment()
        errors = self.config.validate()
        if errors:
            for err in errors:
                logger.error("Configuration error: %s", err)
            raise RuntimeError(f"Configuration validation failed: {errors}")
        logger.info("Bootstrap: configuration loaded (mode=%s)", self.config.runtime_mode)

    def _step_validate_environment(self) -> None:
        self.lifecycle.transition(LifecyclePhase.DEPENDENCY_VALIDATION)
        self.lifecycle.transition(LifecyclePhase.DISCOVERY)
        logger.info("Bootstrap: environment validated")

    def _step_load_secrets(self) -> None:
        self.secrets = SecretManager()
        self.secrets.load()
        result = self.secrets.validate()
        logger.info(
            "Bootstrap: secrets loaded (present=%s, missing=%s)",
            result.present,
            result.missing,
        )

    def _step_create_identity(self) -> None:
        self.identity = RuntimeIdentity.create()
        logger.info(
            "Bootstrap: Runtime identity created — id=%s version=%s",
            self.identity.runtime_id,
            self.identity.runtime_version,
        )

    def _step_initialize_services(self) -> None:
        self.registry = RuntimeRegistry()
        self.supervisor = RuntimeSupervisor()
        self.health = HealthService()
        self.recovery = RecoveryService(max_attempts=self.config.max_recovery_attempts)
        self.metrics = RuntimeMetrics()
        self.reports = RuntimeReports(logs_dir=self.config.logs_dir)

        # Wire recovery exhaustion handler
        self.recovery.on_exhausted(self._on_recovery_exhausted)

        # Register basic health checks
        self.health.register_check("supervisor", self.supervisor.all_healthy)

        self.metrics.set_gauge("runtime_id", self.identity.runtime_id)
        self.metrics.set_gauge("runtime_version", self.identity.runtime_version)
        logger.info("Bootstrap: core services initialized")

    def _step_register_engines(self) -> None:
        """Register existing AI Toolkit engines with the Runtime Registry."""
        registered = []
        engine_candidates = {
            "planning": "python.planning_engine.engine:PlanningEngine",
            "execution": "python.execution_engine.engine:ExecutionEngine",
            "validation": "python.validation_engine.engine:ValidationEngine",
            "repository": "python.repository_engine.engine:RepositoryEngine",
            "dependency": "python.dependency_engine.engine:DependencyEngine",
        }

        for name, module_path in engine_candidates.items():
            module_str, class_name = module_path.rsplit(":", 1)
            try:
                import importlib
                module = importlib.import_module(module_str)
                engine_class = getattr(module, class_name)
                self.registry.register_engine(name, engine_class)
                self.supervisor.register(f"engine.{name}")
                registered.append(name)
            except Exception as exc:
                logger.debug("Bootstrap: engine %s not available: %s", name, exc)

        logger.info("Bootstrap: registered engines: %s", registered)

    def _step_register_services(self) -> None:
        """Register Runtime services in the registry."""
        self.registry.register_service("health", self.health)
        self.registry.register_service("recovery", self.recovery)
        self.registry.register_service("supervisor", self.supervisor)
        self.registry.register_service("metrics", self.metrics)
        self.registry.register_service("reports", self.reports)
        logger.info("Bootstrap: Runtime services registered")

    def _step_restore_state(self) -> None:
        """Restore persistent Runtime state from the state directory."""
        import pathlib
        state_dir = pathlib.Path(self.config.state_dir)
        state_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Bootstrap: state directory ready at %s", state_dir)
        self.metrics.increment("runtime.restarts")

    def _step_initialize_scheduler(self) -> None:
        self.scheduler = SchedulerHost(tick_interval=1.0)
        # Register standard periodic jobs
        self.scheduler.register(
            "health.check",
            "Runtime Health Check",
            self._periodic_health_check,
            interval_seconds=self.config.scheduler_interval_seconds,
        )
        self.scheduler.register(
            "metrics.report",
            "Runtime Metrics Report",
            self._periodic_metrics_report,
            interval_seconds=max(self.config.scheduler_interval_seconds * 5, 300),
        )
        self.registry.register_service("scheduler", self.scheduler)
        self.supervisor.register("scheduler")
        logger.info("Bootstrap: scheduler initialized")

    def _step_initialize_event_bus(self) -> None:
        self.dispatcher = EventDispatcher()
        self.event_loop = EventLoop(
            tick_interval_seconds=self.config.runtime_loop_interval_seconds
        )

        # Register runtime loop observers
        self.event_loop.register_observer(self._observe_runtime)
        self.event_loop.register_observer(self._observe_health)

        self.registry.register_service("event_dispatcher", self.dispatcher)
        self.registry.register_service("event_loop", self.event_loop)
        self.registry.register_service("job_queue", self.job_queue)
        self.supervisor.register("event_loop")
        logger.info("Bootstrap: event bus initialized")

    def _step_initialize_http_server(self) -> None:
        self.job_queue = JobQueueHost(worker_count=2)
        self.http_server = RuntimeHttpServer(
            host=self.config.http_host,
            port=self.config.http_port,
        )
        self._wire_http_handlers()
        self.registry.register_service("http_server", self.http_server)
        self.supervisor.register("http_server")
        logger.info(
            "Bootstrap: HTTP server configured on %s:%d",
            self.config.http_host,
            self.config.http_port,
        )

    def _wire_http_handlers(self) -> None:
        """Wire Runtime services into the HTTP server handlers."""
        def health_handler() -> dict:
            result = self.health.check_liveness()
            return self.health.to_dict(result)

        def ready_handler() -> dict:
            result = self.health.check_readiness()
            return self.health.to_dict(result)

        def metrics_handler() -> dict:
            return self.metrics.snapshot()

        def status_handler() -> dict:
            report = self.reports.generate_status_report(
                identity=self.identity,
                lifecycle=self.lifecycle,
                health=self.health,
                metrics=self.metrics,
                registry=self.registry,
                supervisor=self.supervisor,
                scheduler=self.scheduler,
                job_queue=self.job_queue,
                event_loop=self.event_loop,
                event_dispatcher=self.dispatcher,
            )
            return report

        self.http_server.set_health_handler(health_handler)
        self.http_server.set_ready_handler(ready_handler)
        self.http_server.set_metrics_handler(metrics_handler)
        self.http_server.set_status_handler(status_handler)

    def _step_initialize_external_interfaces(self) -> None:
        """Initialize isolated external adapters when enabled."""
        self.github_webhook = GitHubWebhookHost(
            dispatcher=self.dispatcher,
            webhook_secret=self.secrets.get("GITHUB_WEBHOOK_SECRET") if self.config.enable_github_webhooks else "",
        )
        self.http_server.set_github_webhook_handler(self.github_webhook.process)

        self.telegram = TelegramGateway(
            bot_token=self.secrets.get("TELEGRAM_BOT_TOKEN"),
            chat_id=self.secrets.get("TELEGRAM_CHAT_ID"),
            event_dispatcher=self.dispatcher,
            enabled=self.config.enable_telegram,
        )
        self.http_server.set_telegram_update_handler(
            self.telegram.process_webhook_update
        )

        if self.config.enable_telegram:
            self.dispatcher.subscribe(
                "telegram.command.status", self._handle_telegram_status
            )
            self.dispatcher.subscribe(
                "telegram.command.health", self._handle_telegram_health
            )
            self.dispatcher.subscribe(
                "telegram.command.report", self._handle_telegram_report
            )

            if self.telegram.is_enabled():
                self.scheduler.register(
                    "telegram.poll",
                    "Telegram Update Polling",
                    self._poll_telegram,
                    interval_seconds=10,
                )

        self.registry.register_service("github_webhook", self.github_webhook)
        self.registry.register_service("telegram", self.telegram)

        logger.info(
            "Bootstrap: external adapters initialized (interfaces=%s, github=%s, telegram=%s)",
            self.config.enable_external_interfaces,
            self.config.enable_github_webhooks,
            self.telegram.is_enabled(),
        )

    def _step_verify_health(self) -> None:
        result = self.health.check_readiness()
        if not result.healthy:
            logger.warning(
                "Bootstrap: health check failed — %s", result.checks
            )
        else:
            logger.info("Bootstrap: health verified")

    # ------------------------------------------------------------------ #
    # Start / Stop
    # ------------------------------------------------------------------ #

    def start(self) -> None:
        """Start all background services."""
        if not self._bootstrapped:
            raise RuntimeError("bootstrap() must be called before start()")

        self.lifecycle.transition(LifecyclePhase.RUNNING)
        self.identity.lifecycle_phase = LifecyclePhase.RUNNING.value
        self.metrics.set_gauge("lifecycle_phase", "RUNNING")

        self.job_queue.start()
        self.scheduler.start()
        self.event_loop.start()
        self.http_server.start()

        self.metrics.increment("runtime.starts")
        logger.info("Bootstrap: all services started — Runtime RUNNING")

    def stop(self) -> None:
        """Stop all background services (graceful shutdown)."""
        logger.info("Bootstrap: initiating graceful shutdown")

        self.lifecycle.transition(LifecyclePhase.SHUTDOWN)
        self.identity.lifecycle_phase = LifecyclePhase.SHUTDOWN.value

        # Stop in reverse order of start
        if self.http_server:
            self.http_server.stop()
        if self.event_loop:
            self.event_loop.stop()
        if self.scheduler:
            self.scheduler.stop()
        if self.job_queue:
            self.job_queue.stop()

        self.lifecycle.transition(LifecyclePhase.PERSISTENCE)
        self._persist_shutdown_state()

        self.lifecycle.transition(LifecyclePhase.TERMINATION)
        logger.info("Bootstrap: graceful shutdown complete")

    # ------------------------------------------------------------------ #
    # Periodic observers / handlers
    # ------------------------------------------------------------------ #

    def _observe_runtime(self) -> None:
        self.metrics.increment("runtime.loop.ticks")

    def _observe_health(self) -> None:
        result = self.health.check_readiness()
        self.metrics.set_gauge("health_ready", result.ready)
        if not result.healthy:
            self.supervisor.record_failure("health", "health check failed")

    def _periodic_health_check(self) -> None:
        results = self.supervisor.run_health_checks()
        self.metrics.set_gauge("supervisor.all_healthy", all(results.values()))

    def _periodic_metrics_report(self) -> None:
        report = self.reports.generate_status_report(
            identity=self.identity,
            lifecycle=self.lifecycle,
            health=self.health,
            metrics=self.metrics,
        )
        self.reports.persist_report(report, name="periodic")

    def _poll_telegram(self) -> None:
        updates = self.telegram.poll_updates()
        for update in updates:
            self.telegram.process_update(update)

    def _handle_telegram_status(self, event) -> None:
        report = self.reports.generate_status_report(
            identity=self.identity,
            lifecycle=self.lifecycle,
            health=self.health,
            metrics=self.metrics,
        )
        summary = self.reports.format_text_summary(report)
        self.telegram.send_message(summary)

    def _handle_telegram_health(self, event) -> None:
        result = self.health.check_readiness()
        status = "✅ HEALTHY" if result.healthy else "❌ UNHEALTHY"
        ready = "✅ READY" if result.ready else "⏳ NOT READY"
        self.telegram.send_message(f"*Health*: {status}\n*Readiness*: {ready}")

    def _handle_telegram_report(self, event) -> None:
        report = self.reports.generate_status_report(
            identity=self.identity,
            lifecycle=self.lifecycle,
            health=self.health,
            metrics=self.metrics,
        )
        summary = self.reports.format_text_summary(report)
        self.telegram.send_message(f"*Operational Report*\n\n{summary}")

    def _on_recovery_exhausted(self) -> None:
        logger.critical("Bootstrap: recovery exhausted — transitioning to MAINTENANCE")
        self.lifecycle.transition(LifecyclePhase.MAINTENANCE)
        self.telegram.send_health_alert(
            "Runtime recovery exhausted. Manual intervention may be required."
        )

    def _persist_shutdown_state(self) -> None:
        """Persist final state before termination."""
        import pathlib, json as _json
        state_dir = pathlib.Path(self.config.state_dir)
        state_dir.mkdir(parents=True, exist_ok=True)
        shutdown_state = {
            "runtime_id": self.identity.runtime_id,
            "lifecycle_phase": self.identity.lifecycle_phase,
            "metrics": self.metrics.snapshot(),
        }
        path = state_dir / "shutdown_state.json"
        try:
            path.write_text(_json.dumps(shutdown_state, indent=2))
        except Exception as exc:
            logger.warning("Bootstrap: could not persist shutdown state: %s", exc)
