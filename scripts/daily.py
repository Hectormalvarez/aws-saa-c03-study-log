"""The one daily command. Interleaved, capped, pretest-first.

Usage:
  python3 scripts/daily.py           # morning drill: due cards + scenarios + design prompt
  python3 scripts/daily.py --micro   # pre-sleep: recall TODAY's cards only (<=10)
  python3 scripts/daily.py --prompt  # just give a free-recall design prompt
  python3 scripts/daily.py --plan    # miss-cluster analysis for the prescription
"""
import sys
import os
import json
import random
import argparse
import re
from datetime import date, timedelta

import common as C


def plan():
    cfg = C.load_config()
    cards = C.load_cards()
    print(f"=== PRESCRIPTION INPUTS — {date.today().isoformat()} — "
          f"{C.days_to_exam(cfg)} days to exam ===")
    by_domain = {}
    for c in cards:
        d = by_domain.setdefault(c["domain"], {"requeued": [], "learning": [], "unseen": 0})
        if c["reps"] == 0:
            d["unseen"] += 1
        elif c["streak"] == 0:
            d["requeued"].append(c["q"])
        else:
            d["learning"].append((c["id"], c["box"]))
    print("\n-- Card state by domain --")
    for dom in sorted(by_domain):
        d = by_domain[dom]
        line = f"{C.DOMAIN_LABELS.get(dom, dom)}: {len(d['requeued'])} requeued, " \
               f"{len(d['learning'])} in rotation, {d['unseen']} unseen"
        print(line)
        for q in d["requeued"]:
            print(f"   ✘ {q}")
    misses = []
    try:
        text = open(C.WRONG_PATH).read()
        cutoff = (date.today() - timedelta(days=2)).isoformat()
        misses = re.findall(rf"## ({cutoff}|{cutoff}|{date.today().isoformat()})\S* — scenario `([^`]+)`", text)
        scen = re.findall(r"## \d{4}-\d{2}-\d{2} — scenario `([^`]+)`", text)
        if scen:
            print(f"\n-- Scenario misses logged: {len(scen)} (ids: {', '.join(scen)}) --")
    except FileNotFoundError:
        print("\n-- No scenario misses logged --")
    attempts = []
    if os.path.exists(C.ATTEMPTS_PATH):
        with open(C.ATTEMPTS_PATH) as f:
            attempts = json.load(f)
    if attempts:
        print("\n-- Latest mock:", attempts[-1].get("overall_pct", "?"), "% overall --")
    print("\nTonight's mechanical priorities: requeued cards above + weakest domain by "
          "requeued count + any missed scenario topics.")



def scenario_q(q, cfg):
    print(f"\nSCENARIO [{q['domain']}] services: {', '.join(q.get('services', []))}")
    print(f"  {q['q']}")
    for i, opt in enumerate(q["options"]):
        print(f"    {i}) {opt}")
    while True:
        pick = C.safe_input("  Your pick [0-3] (pretest: guessing is GOOD) ").strip()
        if pick in ("0", "1", "2", "3"):
            pick = int(pick)
            break
    correct = pick == q["answer"]
    if correct:
        print("  ✔ Correct.")
    else:
        print(f"  ✘ Correct was ({q['answer']}): {q['options'][q['answer']]}")
    print(f"  Why: {q['explanation']}")
    return correct


def design_prompts():
    p = os.path.join(C.ROOT, "domains", "*", "checklist.md")
    prompts = [
        "Design a 3-tier web app (ALB, ASG, RDS) for HA across 2 AZs. Write every service and why from memory.",
        "A company needs to serve static assets globally with low latency and protect against L7 attacks. Design it from memory.",
        "A nightly batch job processes millions of records, sometimes running 30+ minutes per item. Design the pipeline from memory.",
        "Design a cost-optimal storage lifecycle for access logs: hot for 1 week, instantly retrievable for 1 year, then nearline.",
        "A spiky SaaS API has unpredictable relational DB load. Design the database layer and justify it from memory.",
        "Write the 4 DR strategies with RTO ordering and when each is the exam answer. From memory.",
    ]
    idx = date.today().toordinal() % len(prompts)
    return prompts[idx]


def do_cards(cards, cfg, limit):
    due = C.due_cards(cards)
    random.shuffle(due)
    due = due[:limit]
    if not due:
        print("No cards due — good schedule discipline. Use --all in quiz.py to force.")
        return 0, 0
    n = correct = 0
    for card in due:
        print(f"\n[{card['domain']}] {card['q']}")
        C.safe_input("  recall from memory, then Enter... ")
        print(f"  A: {card['a']}")
        g = C.safe_input("  right? [y/n] ").strip().lower()
        ok = g == "y"
        C.schedule(card, cfg, ok)
        card["last_seen"] = date.today().isoformat()
        n += 1
        correct += ok
        if not ok:
            C.log_wrong("card", card["id"], card["q"], "-", card["a"])
    C.save_cards(cards)
    return n, correct


def do_scenarios(cfg, limit):
    qs = C.load_domain_questions()
    random.shuffle(qs)
    qs = qs[:limit]
    n = correct = 0
    for q in qs:
        ok = scenario_q(q, cfg)
        n += 1
        correct += ok
        if not ok:
            C.log_wrong("scenario", q["id"], q["q"], "-", q["explanation"])
    return n, correct


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--micro", action="store_true", help="pre-sleep recall of today's cards")
    ap.add_argument("--prompt", action="store_true", help="print today's design prompt only")
    ap.add_argument("--plan", action="store_true", help="miss-cluster analysis for tonight's prescription")
    args = ap.parse_args()
    cfg = C.load_config()
    cards = C.load_cards()

    if args.plan:
        plan()
        return

    if args.prompt:
        print(design_prompts())
        return

    if args.micro:
        today = date.today().isoformat()
        touched = [c for c in cards if c.get("last_seen", "").startswith(today)]
        random.shuffle(touched)
        touched = touched[: cfg["session_caps"]["presleep_max_cards"]]
        if not touched:
            print("No cards were seen today. Recall 3 things you learned today from memory instead.")
            return
        n = correct = 0
        print(f"Pre-sleep recall: {len(touched)} cards from today.")
        for card in touched:
            print(f"\n{card['q']}")
            C.safe_input("  recall, then Enter... ")
            print(f"  A: {card['a']}")
            g = C.safe_input("  right? [y/n] ").strip().lower()
            ok = g == "y"
            n += 1
            correct += ok
            if not ok:
                C.log_wrong("card", card["id"], card["q"], "-", card["a"])
        C.append_log({"kind": "micro", "n": n, "correct": correct})
        print(f"\nLogged micro recall: {correct}/{n}. Sleep well — consolidation ahead.")
        return

    caps = cfg["session_caps"]
    print(f"=== DAILY DRILL — {date.today().isoformat()} — "
          f"{C.days_to_exam(cfg)} days to exam ===")
    n1, c1 = do_cards(cards, cfg, caps["max_cards_per_session"])
    n2, c2 = do_scenarios(cfg, caps["max_scenario_questions"])
    print("\n=== DESIGN PROMPT (write it in practice/answers/, from memory) ===")
    print(design_prompts())
    C.append_log({"kind": "daily", "cards_n": n1, "cards_correct": c1,
                  "scen_n": n2, "scen_correct": c2})
    total, correct = n1 + n2, c1 + c2
    if total:
        print(f"\nSession: {correct}/{total} ({100 * correct // total}%). "
              f"Commit when done. Struggle is the point.")


if __name__ == "__main__":
    main()
