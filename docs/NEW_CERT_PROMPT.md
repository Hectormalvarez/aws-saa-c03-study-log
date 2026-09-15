# Prompt: Stand Up a Study Sprint Repo for a New Certificate

Use this prompt with an AI coding agent. Replace every `<ANGLE-BRACKET>` field first.

---

You are building me an exam-prep sprint repo. Follow this spec exactly.

## Context (fill in)
- **Certificate:** <NAME + EXAM CODE, e.g. "AWS Certified Developer Associate DVA-C02">
- **My prep status:** <already watched a course / starting from zero>
- **Start date:** <DATE> — **Target exam:** <DATE ~2 weeks out> — **Flex date:** <DATE ~4 weeks out>
- **My work schedule:** <hours + wake time> — schedule sessions around peaks (mid-morning and early-evening deep work; avoid quizzing within 1h of waking)
- **Practice materials:** <e.g. Udemy practice tests + AI-generated question sets>

## Science-based design rules (non-negotiable)
1. **Retrieval practice first** — every session quizzes before it teaches. Notes exist only to check answers against.
2. **Spaced repetition** — Leitner boxes (0–4) with intervals computed RELATIVE to days-until-exam (~10–20% of remaining time, Cepeda 2008), so the schedule compresses near the exam. Wrong answers → box 0, due tomorrow.
3. **Interleaving** — daily drills mix domains; never block-review one topic per session.
4. **Desirable difficulty** — free recall (type your answer) beats recognition. Pretesting: scenario questions may be attempted before studying the topic.
5. **Pre-sleep consolidation** — a `--micro` mode recalling only today's cards (≤10), 2 minutes, before bed.
6. **Metacognition guard** — go/no-go SIT/EXTEND decisions come from logged mock scores at fixed checkpoint days, never from confidence.
7. **Commit after every session** — git history IS the study log.

## Required structure
```
<repo-name>/
├── README.md                  # exam facts (format, # questions, time, pass score, domain weights),
│                              # daily ritual table, checkpoint rules, science summary, commands
├── config.json                # exam dates, start date, session caps, checkpoint thresholds,
│                              # Leitner intervals + compressed multipliers, mock sources
├── domains/                   # one folder per exam domain, named with weight, e.g. 01-secure-30pct/
│   ├── checklist.md           # EVERY official task statement as "- [ ]" checkboxes
│   └── questions.json         # scenario MCQs: id, domain, services/topics, q, options, answer idx,
│                              # explanation (why right AND why others wrong)
├── services/ or topics/       # cheat sheets + comparison tables of similar concepts
├── flashcards/cards.json      # cards: id, domain, q, a, box, due, streak, reps, last_seen
├── practice/
│   ├── wrong-answers.md       # auto-appended on every miss: date, Q, my answer, correct, why
│   └── answers/               # dated written design answers (free recall), gitignored
├── progress/
│   ├── attempts.json          # mock log: date, day#-to-exam, per-domain scores, overall %
│   └── log.jsonl              # auto session log (gitignored)
├── docs/
└── scripts/                   # stdlib-only Python, no third-party deps
```

## Required scripts
- `common.py` — config/loader helpers, Leitner interval math scaled to exam date, jsonl logging, safe_input (graceful Ctrl-D)
- `quiz.py` — `--due` (default), `--topic <domain>`, `--all`, `--stats` (by box/domain); self-graded cards
- `daily.py` — THE daily command: due cards (capped ~25, shuffled/interleaved) → N scenario questions (pretest framing) → print a free-recall design/essay prompt (deterministic by date); `--micro` for pre-sleep; `--prompt` to print prompt only
- `exam_log.py` — `log` (interactive per-domain scores), `list`, `reco`: SIT if checkpoint-day score ≥ threshold, EXTEND if < floor, borderline → re-mock; ALWAYS print weakest 2 domains as tonight's priorities
- `progress.py` — checklist coverage bars, drill streak from log.jsonl, accuracy by session kind

## Build process (do this, in order)
1. Ask me for the official exam guide content (or fetch it): domain weights and the full task-statement list. If unavailable, ask me to paste it — never invent task statements.
2. Plan mode: present the repo layout + daily schedule adapted to my work hours; get approval.
3. Act mode, committing after each coherent unit:
   a. skeleton + README + config.json
   b. domain checklists (verbatim task statements) + question decks (3–5 seeded MCQs per domain, real exam style, with explanations)
   c. cheat sheets/comparisons for the top confusable concepts + seed flashcards (~4–6 per domain)
   d. scripts (common → quiz → daily → exam_log → progress)
4. **Verify before finishing:** compile all scripts; run a piped end-to-end simulation of daily.py and daily.py --micro; test exam_log.py reco with a sample attempt; reset all test state (cards to box 0 / due = start date, delete test logs) so day 1 is pristine.
5. Verify final deck/config JSON validity and report what I should run on day 1.

## Checkpoint config (2-week sprint template)
- day_4_min_pct: 65 (mock 1 — below this is expected, keep going)
- day_8_sit_pct: 75, day_8_extend_floor_pct: 70 (decision window day 6–10 only)
- Flex plan: if extended, stretch intervals, second pass on weak domains, 3 more mocks

## Daily ritual template (adapt to my hours)
| Slot | What |
|---|---|
| Morning (~25 min) | `daily.py` — due cards + scenarios + design prompt → commit |
| Midday (~10 min) | `quiz.py --due` to clear same-day requeues |
| Evening block 1 | New domain topics, retrieval-first (attempt before reading) |
| Evening block 2 | Author new cards/questions (AI OK — I vet every answer), force-drill weakest domain, write design answer, tick cold-verifiable checklist items → commit |
| Pre-sleep (~2 min) | `daily.py --micro` |

## Rules for me (include in README)
- First-attempt mock scores of 55–70% after a course are expected data, not failure
- If a drill feels smooth, difficulty is too low — that's the fluency illusion
- Never cram; pre-sleep micro-recall + sleep > late-night extra hour
- Every AI-generated question gets vetted before entering the scheduler
- One commit per session, message like `study(day N): <accuracy>% — <weak domain>`
