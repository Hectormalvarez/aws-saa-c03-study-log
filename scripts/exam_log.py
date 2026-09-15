"""Mock-exam log + go/no-go recommendation (SIT / EXTEND).

Usage:
  python3 scripts/exam_log.py log          # record a mock attempt (interactive)
  python3 scripts/exam_log.py list         # show attempts
  python3 scripts/exam_log.py reco         # SIT/EXTEND recommendation + weak domains
"""
import json
import os
import argparse
from datetime import date

import common as C


def load_attempts():
    if not os.path.exists(C.ATTEMPTS_PATH):
        return []
    with open(C.ATTEMPTS_PATH) as f:
        return json.load(f)


def save_attempts(a):
    with open(C.ATTEMPTS_PATH, "w") as f:
        json.dump(a, f, indent=2)


def log():
    cfg = C.load_config()
    attempts = load_attempts()
    print("Enter per-domain scores as 'correct/total', or blank to skip.")
    print("Domains:", ", ".join(C.DOMAINS))
    attempt = {"date": date.today().isoformat(), "days_to_exam": C.days_to_exam(cfg), "domains": {}}
    tot_c = tot_n = 0
    for d in C.DOMAINS:
        raw = input(f"  {C.DOMAIN_LABELS[d]}: ").strip()
        if not raw:
            continue
        c, n = [int(x) for x in raw.split("/")]
        attempt["domains"][d] = {"correct": c, "total": n}
        tot_c += c
        tot_n += n
    if tot_n:
        attempt["overall_pct"] = round(100 * tot_c / tot_n)
    attempts.append(attempt)
    save_attempts(attempts)
    print(f"Logged: {attempt['overall_pct']}% overall." if tot_n else "Logged (no scores).")


def reco():
    cfg = C.load_config()
    attempts = load_attempts()
    if not attempts:
        print("No attempts logged yet. Run: python3 scripts/exam_log.py log")
        return
    latest = attempts[-1]
    pct = latest.get("overall_pct", 0)
    day_n = None
    start = date.fromisoformat(cfg["start_date"])
    d = date.fromisoformat(latest["date"])
    day_n = (d - start).days + 1
    cp = cfg["checkpoints"]
    print(f"Latest attempt: day {day_n}, {pct}% overall")
    if pct < cp["day_4_min_pct"]:
        print(f"Below {cp['day_4_min_pct']}% — expected for first mocks. Keep going; "
              "prioritize weakest domains tonight.")
    if day_n is not None and 6 <= day_n <= 10:
        if pct >= cp["day_8_sit_pct"]:
            print(f"VERDICT: SIT — {pct}% >= {cp['day_8_sit_pct']}%. Final days: "
                  "two more mocks + weak-domain drills.")
        elif pct < cp["day_8_extend_floor_pct"]:
            print(f"VERDICT: EXTEND — {pct}% < {cp['day_8_extend_floor_pct']}%. "
                  f"Move exam to {cfg['flex_exam_date']}: stretch spacing, second pass, 3 more mocks.")
        else:
            print(f"VERDICT: borderline ({pct}%, floor {cp['day_8_extend_floor_pct']}%, "
                  f"sit {cp['day_8_sit_pct']}%). Re-mock in 24-48h and re-run reco.")
    else:
        print(f"VERDICT: on track, no auto-decision yet (decision window: day 6-10). Keep the daily ritual.")
    # weak domains
    scores = []
    for d, s in latest["domains"].items():
        if s["total"]:
            scores.append((100 * s["correct"] / s["total"], d))
    if scores:
        scores.sort()
        print("\nPriority tonight (weakest first):")
        for pct_d, d in scores[:2]:
            print(f"  {C.DOMAIN_LABELS[d]}: {pct_d:.0f}%")


def listing():
    for a in load_attempts():
        print(f"{a['date']}  day-{a.get('days_to_exam')}  {a.get('overall_pct', '-')}%  "
              f"{json.dumps(a.get('domains', {}))}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["log", "list", "reco"])
    args = ap.parse_args()
    {"log": log, "list": listing, "reco": reco}[args.cmd]()
