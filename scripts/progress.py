"""Tracker coverage + streak stats.

Usage:
  python3 scripts/progress.py
"""
import os
import re
import glob

import common as C


def tracker_coverage():
    total = done = 0
    print("Tracker coverage (task statements verified from memory):")
    for d in C.DOMAINS:
        p = os.path.join(C.ROOT, "domains", d, "checklist.md")
        if not os.path.exists(p):
            print(f"  {C.DOMAIN_LABELS[d]}: no checklist")
            continue
        text = open(p).read()
        boxes = re.findall(r"^- \[( |x)\]", text, re.M)
        x = boxes.count("x")
        total += len(boxes)
        done += x
        bar = "#" * x + "." * (len(boxes) - x)
        print(f"  {C.DOMAIN_LABELS[d]:22} [{bar}] {x}/{len(boxes)}")
    if total:
        print(f"  TOTAL: {done}/{total} ({100 * done / total:.0f}%)")


def drill_stats():
    log = C.load_log()
    streak, last = C.streak_days(log)
    print(f"\nDrill streak: {streak} day(s), last session {last or '-'}")
    kinds = {}
    for e in log:
        k = e["kind"]
        a = kinds.setdefault(k, [0, 0])
        a[0] += e.get("n", 0) + e.get("cards_n", 0) + e.get("scen_n", 0)
        a[1] += e.get("correct", 0) + e.get("cards_correct", 0) + e.get("scen_correct", 0)
    for k, (n, c) in kinds.items():
        if n:
            print(f"  {k}: {n} items, {100 * c / n:.0f}% correct")
    answers = glob.glob(os.path.join(C.ROOT, "practice", "answers", "*.md"))
    print(f"Written design answers: {len(answers)}")


if __name__ == "__main__":
    tracker_coverage()
    drill_stats()
