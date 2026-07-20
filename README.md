# Access Control Audit

Tests a technical control objective (least-privilege access + MFA on
privileged accounts) against a sample user access listing, flags
exceptions, and documents the results in an audit workpaper.

## Project structure
```
Access-Control-Audit/
├── README.md
├── data/user_access.csv              # Sample user access listing
├── src/access_review.py              # Runs the control test
└── reports/
    ├── access_review_findings.csv    # Generated on run
    └── Access_Control_Workpaper.md    # Written audit workpaper
```

## Control objective tested
"Access to systems is granted based on job role (least privilege), and
privileged accounts are protected by multi-factor authentication."

## How to run
```bash
python src/access_review.py
```

Reads `data/user_access.csv`, evaluates each account against the control
objective, prints exceptions, and writes them to
`reports/access_review_findings.csv`.

## Result
4 of 10 accounts tested resulted in an exception (excessive privilege,
missing MFA, stale accounts, or access not removed after termination).
Full findings and recommendations are in
`reports/Access_Control_Workpaper.md`.
