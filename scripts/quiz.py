"""Spaced-repetition quiz engine (Leitner boxes, exam-relative intervals).

Usage:
  python3 scripts/quiz.py            # quiz all due cards
  python3 scripts/quiz.py --due      # same as default
  python3 scripts/quiz.py --topic 01-secure
  python3 scripts/quiz.py --stats    # accuracy by box and domain
  python3 scripts/quiz.py --all      # ignore due dates (drill everything)
"""
import sys
import random
import argparse
from datetime import date, timedelta

import common as C


def ask(card):
    print(f"\n[{card['domain']}] {card['q']}")
    C.safe_input("  (press Enter to reveal) ")
    print(f"  A: {card['a']}")
    while True:
        g = C.safe_input("  Did you get it right? [y/n] ").strip().lower()
        if g in ("y", "n"):
            return g == "y"


def run(cards, cfg, limit):
    due = C.due_cards(cards)
    random.shuffle(due)
    due = due[:limit]
    if not due:
        print("Nothing due. Study new material or use --all.")
        return
    print(f"{len(due)} card(s) due. Answer from MEMORY before revealing.")
    correct = 0
    for card in due:
        ok = ask(card)
        C.schedule(card, cfg, ok)
        if ok:
            correct += 1
        else:
            C.log_wrong("card", card["id"], card["q"], "-", card["a"])
    C.save_cards(cards)
    C.append_log({"kind": "quiz", "n": len(due), "correct": correct})
    print(f"\nDone: {correct}/{len(due)} correct. Cards saved.")


def stats(cards):
    by_box, by_domain = {}, {}
    for c in cards:
        b = by_box.setdefault(c["box"], [0, 0, 0])  # count, reps, streak-sum
        b[0] += 1
        b[1] += c["reps"]
        d = by_domain.setdefault(c["domain"], [0, 0])
        d[0] += 1
        d[1] += c["reps"]
    print("By box (box: #cards, total reps):")
    for b in sorted(by_box):
        print(f"  box {b}: {by_box[b][0]} cards, {by_box[b][1]} reps")
    print("By domain (domain: #cards, total reps):")
    for d in sorted(by_domain):
        print(f"  {C.DOMAIN_LABELS.get(d, d)}: {by_domain[d][0]} cards, {by_domain[d][1]} reps")
    due = C.due_cards(cards)
    print(f"\nDue now: {len(due)} / {len(cards)} cards")
    days = C.days_to_exam(C.load_config())
    print(f"Days to target exam: {days}")
    if due:
        soonest = min(c["due"] for c in due)
        print(f"Oldest overdue: {soonest}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", help="restrict to a domain folder name")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--due", action="store_true")
    args = ap.parse_args()
    cfg = C.load_config()
    cards = C.load_cards()
    if args.topic:
        cards = [c for c in cards if c["domain"] == args.topic]
    if args.stats:
        stats(cards)
        return
    limit = cfg["session_caps"]["max_cards_per_session"]
    if args.all:
        random.shuffle(cards)
        run_forced(cards, cfg, limit)
        return
    run(cards, cfg, limit)


def run_forced(cards, cfg, limit):
    subset = cards[:limit]
    correct = 0
    for card in subset:
        ok = ask(card)
        C.schedule(card, cfg, ok)
        correct += ok
    C.save_cards(cards)
    C.append_log({"kind": "quiz", "n": len(subset), "correct": correct, "forced": True})
    print(f"\nDone: {correct}/{len(subset)} correct.")


if __name__ == "__main__":
    main()
