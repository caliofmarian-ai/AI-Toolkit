# CANON-022 — Project Memory Specification

Version: 1.0.0

Status: Draft

Priority: Critical

---

# Purpose

Define the persistent memory model used by the AI CTO Platform.

The objective is to allow every managed project to resume development at any time without requiring the owner to manually explain previous work.

Project Memory becomes the long-term memory of the Development Brain.

---

# Mission

Maintain complete project continuity across sessions, deployments and AI executors.

---

# Objectives

Project Memory shall:

- survive restarts
- survive redeployments
- survive repository updates
- survive AI model changes
- survive executor changes
- preserve architectural context
- preserve development history
- preserve decisions
- preserve priorities

---

# Memory Scope

Every managed repository shall own an independent Project Memory.

Project Memory shall include:

Project Metadata

Architecture State

Canonical State

Development Progress

Open Tasks

Completed Tasks

Pending Reviews

Open Pull Requests

Known Risks

Repository Health

Owner Decisions

Learning History

---

# Repository Context

Maintain:

repository

branch

latest commit

latest tag

default branch

working branch

repository profile

---

# Canonical Context

Maintain:

implemented specifications

missing specifications

coverage

compliance

architecture drift

dependency graph

last canonical audit

---

# Development Context

Maintain:

current milestone

current batch

next batch

estimated effort

development velocity

blocked work

completed work

---

# AI Context

Maintain:

preferred executor

executor history

execution success rate

estimated execution quality

execution costs

---

# Decision Memory

Persist:

accepted recommendations

rejected recommendations

manual overrides

architecture decisions

planning decisions

priority changes

---

# Daily State

Remember:

last working session

last repository

last activity

pending work

recommended next action

---

# Resume Capability

The platform shall support:

Continue Project

Continue Repository

Continue Batch

Continue Pull Request

Continue Review

Continue Planning

without requiring manual context reconstruction.

---

# Telegram Integration

The Telegram Dashboard shall provide:

Continue

Resume Yesterday

Current Status

Project Summary

Pending Reviews

Today's Recommendation

---

# Observability

Expose:

memory size

last update

repository count

decision count

resume success rate

knowledge freshness

---

# Invariants

Project Memory shall never be lost.

Memory shall be versioned.

Memory shall remain explainable.

Every recommendation shall reference Project Memory.

---

# Future Evolution

Future versions may include:

conversation memory

meeting memory

team memory

cross-user memory

predictive memory

knowledge aging

---

# Dependencies

Depends on:

CANON-020

CANON-021

Supports:

Development Brain

Telegram Dashboard

AI CTO Platform

Autonomous Development
