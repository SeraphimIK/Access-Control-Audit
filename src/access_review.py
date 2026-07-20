"""
Access Control Audit
--------------------
Tests user access against a least-privilege control objective: administrator
access should be limited to IT roles, accounts should show recent activity,
and privileged access should require MFA. Flags exceptions and writes an
audit workpaper-style findings file.

Control objective tested:
  "Access to systems is granted based on job role (least privilege), and
   privileged accounts are protected by multi-factor authentication."

Run from the repository root:
    python src/access_review.py
"""

import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "data", "user_access.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "reports", "access_review_findings.csv")

IT_ROLES = {"System Administrator", "Help Desk Tech", "Network Engineer"}
STALE_LOGIN_THRESHOLD_DAYS = 60


def evaluate_row(row):
    exceptions = []

    if row["access_level"] == "Administrator" and row["job_role"] not in IT_ROLES:
        exceptions.append("Excessive privilege: admin access without IT role")

    if row["access_level"] == "Administrator" and row["mfa_enabled"] == "No":
        exceptions.append("Privileged account without MFA")

    if int(row["last_login_days_ago"]) > STALE_LOGIN_THRESHOLD_DAYS:
        exceptions.append(f"Stale account: no login in {row['last_login_days_ago']} days")

    if row["job_role"] == "Former Employee":
        exceptions.append("Access not deprovisioned after termination")

    return exceptions


def run_review():
    findings = []
    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            exceptions = evaluate_row(row)
            if exceptions:
                findings.append({
                    "user_id": row["user_id"],
                    "user_name": row["user_name"],
                    "system": row["system"],
                    "access_level": row["access_level"],
                    "exceptions": "; ".join(exceptions),
                })

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["user_id", "user_name", "system", "access_level", "exceptions"])
        writer.writeheader()
        writer.writerows(findings)

    print("=" * 70)
    print("ACCESS CONTROL AUDIT - EXCEPTION FINDINGS")
    print("=" * 70)
    for row in findings:
        print(f"{row['user_name']:<15} {row['system']:<20} {row['exceptions']}")
    print("-" * 70)
    print(f"Total accounts reviewed: {sum(1 for _ in open(INPUT_FILE)) - 1}")
    print(f"Exceptions found: {len(findings)}")
    print(f"Findings written to {OUTPUT_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    run_review()
