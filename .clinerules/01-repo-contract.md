---
applies:
  paths: ["**"]
---

# Study Repo Contract

This is a certificate study sprint repo. The Cline study personas operate here;
all state lives in the repo, scripts own scheduler state.

- Read `SPRINT.md` first — it carries day, phase, checkpoints, and verdicts.
- Config machine-truth is `config.json`; do not hand-edit scheduler state in
  `flashcards/*.json` or `progress/log.jsonl` — always go through `scripts/`.
- Checklists (`domains/*/checklist.md`) are ticked only on my cold recall — never
  on your assessment of what I "probably know".
- Commands: `python3 scripts/daily.py` (morning; `--micro` pre-sleep, `--plan` analysis),
  `scripts/quiz.py --due|--topic <domain>|--stats`, `scripts/exam_log.py log|list|reco`,
  `scripts/progress.py`.
- Scenario decks: `domains/<domain>/questions.json`. Flashcards: `flashcards/<domain>.json`.
- New AI-authored content waits at the human vet gate before entering decks
  (persona-content-author procedure).
