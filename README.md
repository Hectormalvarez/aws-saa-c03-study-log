# AWS SAA-C03 Exam Sprint Repo

**Target:** AWS Certified Solutions Architect – Associate (SAA-C03)
**Sprint:** 14 days (Mon 2026-09-15 → Mon 2026-09-28), flex to 4 weeks (Mon 2026-10-12)
**Basis:** course already watched → this is a *verification and retrieval* sprint, not first-pass learning.

## Exam facts
- 65 questions, 130 minutes, pass ~720/1000
- Domains: Secure Architectures 30% · Resilient Architectures 26% · High-Performing 24% · Cost-Optimized 20%
- Scenario-driven: pick the *right* service among similar ones under given constraints

## The science this repo is built on
- **Retrieval practice** — testing *is* studying; recall beats restudy (Roediger & Karpicke 2006; Dunlosky 2013)
- **Spacing** — review gaps ≈ 10–20% of time-to-exam; at 14 days that means ~1–3 day cycles (Cepeda 2008)
- **Interleaving** — mixed-topic drills beat blocked practice for exactly the discrimination skill this exam tests (Rohrer)
- **Desirable difficulty** — if the drill feels smooth, it's probably not working; free recall > MCQ (Bjork)
- **Pre-sleep retrieval** — a 2-min recall of tonight's material before bed rides slow-wave consolidation (Gais, Lucas & Born 2006)
- **Metacognition trap** — track scores, not confidence; `exam_log.py` makes the sit/extend call

## Daily ritual (6:30–15:00 work day, wake 4–5am)

| Slot | Time | What |
|---|---|---|
| Morning drill | ~06:00 | `python3 scripts/daily.py` — due cards + pretest scenarios (~25 min) |
| Lunch micro | midday | 10-min recall of morning material |
| Deep block 1 | 17:30–19:30 | New domain topics (retrieval-first: attempt before reading) |
| Deep block 2 | 20:00–21:30 | Author questions/cards for tonight's topic, mixed quiz, AI-generated drills |
| Pre-sleep | ~21:00 | `python3 scripts/daily.py --micro` — recall of today only (≤10 cards) |
| Weekend | ~6 hrs | Domain sweeps + timed mock + wrong-answer review |

**Commit after every session.** Git history = study log.

## Sprints & checkpoints
- Day 4 mock ≥ 65% → on track
- Day 8 mock ≥ 75% → SIT on day 14
- Day 8 mock < 70% → EXTEND to 4-week plan (spacing stretches, 3 more mocks)
- First-attempt scores of 55–70% are *expected*; the day-4 number is data, not judgment.

## AI-generated testing workflow
Evening block 2: generate 5–10 scenario questions per new topic against the exam task
statements, then **vet every answer yourself before it enters a deck** — a wrong AI answer
in a spaced-repetition system poisons the schedule. Rules live in `config.json`.

## Commands
```bash
python3 scripts/daily.py            # morning drill: due cards + scenarios + design prompt
python3 scripts/daily.py --micro    # pre-sleep recall of today's material
python3 scripts/quiz.py --stats     # per-box/per-domain accuracy
python3 scripts/exam_log.py log     # record a mock attempt (score per domain)
python3 scripts/exam_log.py reco    # SIT/EXTEND recommendation + weak-domain priorities
python3 scripts/progress.py         # tracker coverage + streaks
```

## Layout
```
domains/          4 exam domains: task-statement checklists + question decks
services/         cheat sheets + comparison tables
flashcards/       spaced-repetition cards (Leitner state lives in the JSON)
practice/         wrong-answers log, written answers, mock attempts
progress/         tracker, attempt log, drill log
scripts/          quiz, daily, progress, exam_log (stdlib-only Python)
docs/             exam guide notes, AI-prompt templates
```
