# Audit Workpaper: Access Control Review (Technical Control)

**Control Objective:** Access to systems is granted based on job role
(least privilege), and privileged accounts are protected by multi-factor
authentication (MFA).

**Control Type:** Technical
**Testing Procedure:**
1. Obtained the user access listing (`data/user_access.csv`) covering all
   systems in scope.
2. For each account, verified that administrator-level access was
   consistent with the user's job role (IT roles only).
3. Verified MFA was enabled for all accounts holding administrator access.
4. Reviewed last-login activity to identify stale accounts (no activity in
   60+ days).
5. Cross-checked accounts against employment status to confirm access was
   deprovisioned upon termination.

**Sample/Population:** 10 user accounts across Finance, IT, Marketing, HR,
and Sales.

## Results

| User | System | Exception |
|---|---|---|
| R. Patel | Finance ERP | Administrator access without an IT role; no MFA enabled |
| S. Nguyen | Finance ERP | Stale account, no login in 90 days |
| D. Kim | Customer Database | Administrator access without an IT role; no MFA enabled; stale account (120 days) |
| L. Ramirez | Finance ERP | Access not deprovisioned after termination |

4 of 10 accounts tested (40%) resulted in an exception.

## Conclusion
The control is **not operating effectively**. Least-privilege assignment
and MFA enforcement are inconsistently applied, and the deprovisioning
process did not remove access for a terminated employee. This represents
a control gap with elevated risk given the systems involved (Finance ERP,
Customer Database).

## Recommendations
1. Downgrade non-IT accounts currently holding administrator access to
   standard user roles, or document a documented business justification.
2. Enforce MFA for all privileged accounts.
3. Implement a formal offboarding checklist item requiring access removal
   confirmation within a defined SLA (e.g., 24 hours of termination).
4. Establish a recurring (quarterly) stale-account review.

**Prepared using:** `src/access_review.py`
**Evidence:** `reports/access_review_findings.csv`
