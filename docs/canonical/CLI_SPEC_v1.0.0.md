# CLI Specification
Version: 1.0.0
Status: CANONICAL
Authority: OWNER

# PURPOSE

This document defines the public command-line interface of AI Toolkit.

The CLI is the only supported entry point for users and AI agents.

No engine shall be executed directly unless explicitly documented.

---

# GENERAL FORMAT

ai <command> [subcommand] [arguments]

Examples:

ai inspect

ai inspect /path/to/repository

ai run 84

ai github issues

---

# CORE COMMANDS

discover

inspect

summary

context

work

issue

plan

execute

review

test

doctor

status

resume

continue

finish

run

---

# GIT COMMANDS

git status

git branch

git log

git remote

git commit

git push

git pull

---

# GITHUB COMMANDS

github issues

github issue

github prs

github milestones

github release

github workflow

---

# OUTPUT RULES

Every command shall:

- display a title
- display progress
- return exit code
- produce structured output
- write logs when applicable

---

# EXIT CODES

0 Success

1 User error

2 Repository error

3 Git error

4 GitHub error

5 Engine failure

10 Internal error

---

# BACKWARD COMPATIBILITY

Public commands shall remain stable throughout version 1.x.

Breaking changes require a major version.

