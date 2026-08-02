# AI Toolkit

Universal development toolkit for Termux, GitHub, Railway and AI-assisted software projects.

## Goals

- One command for every project
- GitHub automation
- Railway automation
- Telegram report utilities
- Repository inspection
- AI study helpers
- Cross-project support

Current status: v0.1.0 (Bootstrap)

## Runtime Layout

AI Toolkit separates persistent source artifacts from generated runtime artifacts.

- **Source Artifacts**: versioned project sources (`bin/`, `docs/`, canonical templates).
- **Generated Artifacts**: implementation outputs stored under `.ai/batches/` (issue checklists, plans, PR metadata, steps).
- **Runtime State**: ephemeral execution data under `.ai/runtime/state/`.
- **Cache**: temporary engine cache under `.ai/runtime/cache/`.
- **Logs**: execution/checkpoint/profiling logs under `.ai/runtime/logs/`.
- **Checkpoints**: runtime checkpoint data under `.ai/runtime/checkpoints/`.
- **Sessions**: runtime session state under `.ai/runtime/sessions/`.
