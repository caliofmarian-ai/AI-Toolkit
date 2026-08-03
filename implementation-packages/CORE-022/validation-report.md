# Validation Report

Generated: 2026-08-03T18:41:20.783032+00:00

## tests/test_runtime_bootstrap.sh

Status: PASSED

```text
2026-08-03 19:41:21,659 INFO     lib.python.runtime.bootstrap — Bootstrap: starting AI CTO Runtime Server (CORE-021)
2026-08-03 19:41:21,660 INFO     lib.python.runtime.bootstrap — Bootstrap: configuration loaded (mode=NORMAL)
2026-08-03 19:41:21,660 INFO     lib.python.runtime.bootstrap — Bootstrap: environment validated
2026-08-03 19:41:21,660 INFO     lib.python.runtime.bootstrap — Bootstrap: secrets loaded (present=[], missing=['GITHUB_TOKEN', 'GITHUB_WEBHOOK_SECRET', 'TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID'])
2026-08-03 19:41:21,661 INFO     lib.python.runtime.bootstrap — Bootstrap: Runtime identity created — id=runtime-e27539782da5 version=3.0.0
2026-08-03 19:41:21,661 INFO     lib.python.runtime.bootstrap — Bootstrap: core services initialized
2026-08-03 19:41:21,766 INFO     lib.python.runtime.bootstrap — Bootstrap: registered engines: ['planning', 'execution', 'validation', 'repository', 'dependency']
2026-08-03 19:41:21,767 INFO     lib.python.runtime.bootstrap — Bootstrap: Runtime services registered
2026-08-03 19:41:21,771 INFO     lib.python.runtime.bootstrap — Bootstrap: state directory ready at .ai/runtime/state
2026-08-03 19:41:21,772 INFO     lib.python.runtime.bootstrap — Bootstrap: scheduler initialized
2026-08-03 19:41:21,773 INFO     lib.python.runtime.bootstrap — Bootstrap: event bus initialized
2026-08-03 19:41:21,773 INFO     lib.python.runtime.bootstrap — Bootstrap: HTTP server configured on 0.0.0.0:19001
2026-08-03 19:41:21,773 INFO     lib.python.runtime.interfaces.telegram_gateway — TelegramGateway: disabled (no token or requests unavailable)
2026-08-03 19:41:21,773 INFO     lib.python.runtime.bootstrap — Bootstrap: external interfaces initialized (github=False, telegram=False)
2026-08-03 19:41:21,774 INFO     lib.python.runtime.bootstrap — Bootstrap: health verified
2026-08-03 19:41:21,774 INFO     lib.python.runtime.bootstrap — Bootstrap: Runtime READY — runtime-e27539782da5
2026-08-03 19:41:21,774 INFO     lib.python.runtime.bootstrap — Bootstrap: initiating graceful shutdown
2026-08-03 19:41:21,774 INFO     lib.python.runtime.interfaces.http_server — RuntimeHttpServer stopped
2026-08-03 19:41:21,774 INFO     lib.python.runtime.event_loop — RuntimeEventLoop stopped after 0 ticks
2026-08-03 19:41:21,774 INFO     lib.python.runtime.scheduler — Scheduler stopped
2026-08-03 19:41:21,774 INFO     lib.python.runtime.job_queue — JobQueue stopped
2026-08-03 19:41:21,781 INFO     lib.python.runtime.bootstrap — Bootstrap: graceful shutdown complete
Bootstrap tests PASSED

```

## tests/test_runtime_health.sh

Status: PASSED

```text
Health tests PASSED
Health check raises raised: division by zero

```

## tests/test_runtime_lifecycle.sh

Status: PASSED

```text
Lifecycle tests PASSED

```

## tests/test_runtime_scheduler.sh

Status: PASSED

```text
  Scheduler: job ran 2 time(s)
Scheduler tests PASSED
Scheduler: job Bad Job raised: intentional error
Scheduler: job Bad Job raised: intentional error

```

## tests/test_runtime_shutdown.sh

Status: PASSED

```text
Graceful shutdown tests PASSED
GracefulShutdown: shutdown callback raised: shutdown error

```

## tests/test_runtime_webhooks.sh

Status: PASSED

```text
GitHub webhook tests PASSED
GitHub webhook: invalid signature for event push
GitHub webhook: JSON parse error: Expecting value: line 1 column 1 (char 0)

```

## tests/test_runtime_telegram.sh

Status: PASSED

```text
Telegram gateway tests PASSED
TelegramGateway: webhook error: Expecting value: line 1 column 1 (char 0)

```

---

Passed: 7
Failed: 0
