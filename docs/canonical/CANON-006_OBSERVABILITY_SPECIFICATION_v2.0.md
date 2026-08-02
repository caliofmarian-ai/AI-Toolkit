# CANON-006 — Observability Specification v2.0

## Status

Canonical

---

# Purpose

The Observability Layer provides complete visibility into every execution performed by AI Toolkit.

Every engine, agent and coordinator must report execution metrics through this layer.

Observability is mandatory.

---

# Goals

Provide real-time visibility for

- execution progress
- active engine
- active repository
- execution phase
- throughput
- ETA
- performance
- resource usage
- checkpoint status

---

# Architecture

Every component reports metrics to the Observability Layer.

The Observability Layer never performs analysis.

It only records, aggregates and exposes metrics.

---

# Mandatory Metrics

Every engine must report

- engine name
- repository
- workspace
- execution phase
- start timestamp
- finish timestamp
- elapsed time
- processed items
- warnings
- errors
- status

---

# Progress Tracking

Every long-running operation must expose

- current item
- processed items
- total items
- percentage
- estimated remaining time
- average throughput

---

# Performance Metrics

Capture

- execution duration
- files per second
- directories per second
- average processing time
- peak processing time

Future support

- CPU
- RAM
- Disk I/O
- Network I/O

---

# ETA

The system should estimate

- remaining files
- remaining tasks
- remaining repositories
- total remaining execution time

ETA should continuously improve during execution.

---

# Checkpoints

Observability tracks

- last checkpoint
- checkpoint frequency
- resume availability
- interrupted executions

---

# Repository Dashboard

Each repository exposes

- health
- score
- current engine
- current phase
- completed engines
- pending engines
- recommendations
- generated batches

---

# Workspace Dashboard

Workspace exposes

- repositories discovered
- repositories completed
- repositories failed
- repositories pending
- total progress
- estimated completion time

---

# Event Logging

Record

INFO

WARNING

ERROR

CRITICAL

Each event includes

- timestamp
- component
- repository
- message

---

# Historical Metrics

Store

- previous execution duration
- previous repository scores
- previous recommendations
- historical trends

---

# Future Dashboards

Support

Terminal Dashboard

Web Dashboard

GitHub Dashboard

Railway Dashboard

REST API

WebSocket Live Updates

---

# API

Observability should expose structured APIs.

No engine should print directly to stdout.

Console output becomes a presentation layer only.

---

# Acceptance Criteria

Every execution is observable.

Every engine exposes metrics.

ETA is continuously updated.

Checkpoint status is visible.

Workspace progress is visible.

Historical metrics are retained.

