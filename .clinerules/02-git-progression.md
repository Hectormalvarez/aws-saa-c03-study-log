---
applies:
  paths: ["**"]
---

# Git as Progression System

In study repos the git log IS the study history. Every session leaves evidence.

- **Every session commits.** Message format: `study(day N): <accuracy>% — <weakest domain>`.
- **Prescriptions are files:** write tonight's plan to `practice/prescriptions/<date>.md`
  and commit it. Tomorrow's session opens it first and verifies execution.
- **Tags mark milestones:** `mock-day<N>` on every mock; `verdict-sit` / `verdict-extend`
  on decisions. Never delete or rewrite study history; append forward.
- **Committed artifacts:** prescriptions, design answers, mock summaries, session log
  (`progress/log.jsonl`), attempts. The repo is the system of record — no study evidence
  lives only in chat.
- **Reconfiguration commits:** date/structure changes get their own `chore(sprint):` commit
  with the reason in `SPRINT.md`.
- Canonical rules live in `ai-prompts/projects/study-repo/rules/`; this copy is re-synced
  from there when updated.
