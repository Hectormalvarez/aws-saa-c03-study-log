"""Shared helpers for aws-saa scripts. Stdlib only."""
import glob
import json
import os
from datetime import date, datetime, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLASHCARDS_DIR = os.path.join(ROOT, "flashcards")
CONFIG_PATH = os.path.join(ROOT, "config.json")
LOG_PATH = os.path.join(ROOT, "progress", "log.jsonl")
ATTEMPTS_PATH = os.path.join(ROOT, "progress", "attempts.json")
WRONG_PATH = os.path.join(ROOT, "practice", "wrong-answers.md")
DOMAINS = ["01-secure", "02-resilient", "03-high-performing", "04-cost-optimized"]
DOMAIN_LABELS = {
    "01-secure": "D1 Secure (30%)",
    "02-resilient": "D2 Resilient (26%)",
    "03-high-performing": "D3 High-Perf (24%)",
    "04-cost-optimized": "D4 Cost (20%)",
}


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def load_cards():
    """Merge all per-domain deck files (flashcards/<domain>.json)."""
    out = []
    for path in sorted(glob.glob(os.path.join(FLASHCARDS_DIR, "*.json"))):
        with open(path) as f:
            out.extend(json.load(f)["cards"])
    return out


def save_cards(cards):
    """Write cards back to their per-domain deck files."""
    by_domain = {}
    for card in cards:
        by_domain.setdefault(card["domain"], []).append(card)
    for domain, domain_cards in by_domain.items():
        path = os.path.join(FLASHCARDS_DIR, f"{domain}.json")
        with open(path, "w") as f:
            json.dump({"cards": domain_cards}, f, indent=2, ensure_ascii=False)


def load_domain_questions():
    """Collect scenario questions from all domain decks."""
    qs = []
    for d in DOMAINS:
        p = os.path.join(ROOT, "domains", d, "questions.json")
        if os.path.exists(p):
            with open(p) as f:
                qs.extend(json.load(f)["questions"])
    return qs


def days_to_exam(cfg, today=None):
    today = today or date.today()
    return (date.fromisoformat(cfg["target_exam_date"]) - today).days


def next_interval_days(cfg, box):
    """Leitner interval scaled to the time remaining until the exam.
    As the exam nears, intervals compress (Cepeda: gap ~10-20% of remaining time)."""
    l = cfg["leitner"]
    if box <= 0:
        return 0
    base = l["base_intervals_days"][min(box, len(l["base_intervals_days"]) - 1)]
    mult = l["compressed_multipliers"][min(box, len(l["compressed_multipliers"]) - 1)]
    interval = base * mult
    remaining = max(days_to_exam(cfg), 1)
    # gap should be 10-20% of remaining time; cap so we don't overshoot
    cap = max(1, int(remaining * 0.2))
    return max(1, min(int(interval) or 1, cap, l["max_interval_days"]))


def promote(card, cfg):
    card["box"] += 1
    card["streak"] += 1


def demote(card):
    card["box"] = 0
    card["streak"] = 0


def schedule(card, cfg, correct):
    card["reps"] += 1
    if correct:
        promote(card, cfg)
    else:
        demote(card)
    card["due"] = (date.today() + timedelta(days=next_interval_days(cfg, card["box"]))).isoformat()


def append_log(entry):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    entry["ts"] = datetime.now().isoformat(timespec="seconds")
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")


def load_log():
    if not os.path.exists(LOG_PATH):
        return []
    out = []
    with open(LOG_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def log_wrong(kind, ref, question, my_answer, correct_answer):
    os.makedirs(os.path.dirname(WRONG_PATH), exist_ok=True)
    with open(WRONG_PATH, "a") as f:
        f.write(
            f"\n## {date.today().isoformat()} — {kind} `{ref}`\n"
            f"- **Q:** {question}\n"
            f"- **My answer:** {my_answer}\n"
            f"- **Correct:** {correct_answer}\n"
            f"- (requeued in scheduler)\n"
        )


def safe_input(prompt):
    try:
        return input(prompt)
    except EOFError:
        print("\n[session ended — progress up to this point is saved]")
        raise SystemExit(0)
    except KeyboardInterrupt:
        print("\n[aborted — progress up to this point is saved]")
        raise SystemExit(130)


def due_cards(cards, today=None):
    today = today or date.today()
    t = today.isoformat()
    return [c for c in cards if c["due"] <= t]


def streak_days(log):
    days = sorted({e["ts"][:10] for e in log})
    if not days:
        return 0, None
    streak = 1
    for prev, cur in zip(days[::-1][1:], days[::-1]):
        if (date.fromisoformat(cur) - date.fromisoformat(prev)).days == 1:
            streak += 1
        else:
            break
    return streak, days[-1]
