# WEEKLY PROJECT VISIBILITY CARD

> **Dev Team Instructions:** Fill out this markdown report every Friday. Do not remove table headers or field labels.

## PROJECT METADATA
- **Company:** TIC INCUBATOR
- **Project ID:** GREYHOUND_APP
- **Client:** GREYHOUND DOG RACE
- **Project Name:** GREYHOUND CUSTOMER MOBILE APP
- **Current Release:** PHASE 1
- **Week No:** 2
- **Reporting Period:** 17–28 AUGUST 2026
- **Week Ending Date:** 28 AUGUST 2026
- **Overall Status:** AMBER <!-- Options: GREEN | AMBER | RED -->

---

## RESOURCE ALLOCATION
- **Total Allocated Man-Days:** 13
- **Release Start Date:** 17 AUGUST 2026

| Resource Name | Role | Allocation (Man-Days) | Main Responsibility |
| :--- | :--- | :---: | :--- |
| Gobithas Kalaimakan | Developer | 13 | Greyhound customer mobile app enhancements / development |

---

## 1. SCOPE & RELEASE JOURNEY

### Delivered Releases
- **N/A**

### Current Release (PHASE 1)
- **Completed This Period:** API wiring updates, QR scan-to-ticket-add flow, response mapping improvements, polling & UX improvements, and development setup fixes.
- **Current Work:** End-to-end validation and stabilization, UI/UX observation for real-world usage, and final bug verification.
- **Upcoming / Pending:** Production SSL / HTTPS validation, final QA and release-readiness checks, and monitoring live behavior after deployment.
- **Integration Status:** Integration improvements completed.

### Future Releases
- **N/A**

---

## 2. CURRENT RELEASE PLAN (PHASE 1 ONLY)

- **Original Plan Start:** 17 AUGUST 2026
- **Original Plan End:** 02 SEPTEMBER 2026
- **Current Forecast Start:** 17 AUGUST 2026
- **Current Forecast End:** N/A
- **Schedule Delay:** N/A
- **Schedule Status:** AT RISK <!-- Options: ON TRACK | AT RISK | OFF TRACK -->

### Milestones Breakdown
| Milestone | Original Plan | Current Forecast | Variance | Status |
| :--- | :--- | :--- | :---: | :---: |
| API Wiring | N/A | Completed | N/A | GREEN |
| QR Scan → Ticket Add Flow | N/A | Completed | N/A | GREEN |
| Response Mapping | N/A | Completed | N/A | GREEN |
| Polling & UX | N/A | Completed | N/A | GREEN |
| Dev Setup | N/A | Completed | N/A | GREEN |
| Production Validation | N/A | In Progress | N/A | AMBER |

### Current Phase Work Items
| Work Item | Category | Status | Remarks |
| :--- | :--- | :---: | :--- |
| API Wiring | Previously Committed | Completed | Base URL and scanner-host integration updated; X-api-key header added and end-to-end behavior verified. |
| QR Scan → Ticket Add Flow | Previously Committed | Completed | Scanned code auto-populates ticket details while allowing user edits; entitlement/API error handling improved. |
| Response Mapping | Enhancement | Completed | Detail, alert and error response handling improved, including clearer messages and error parsing. |
| Polling & UX | Enhancement | Completed | Polling interval changed from 5s to 30s; loading/overlay behavior and retry handling improved. |
| Dev Setup | Support Fix | Completed | Android development setup and supporting service/configuration fixes applied. |
| Production Validation | Release Prep | In Progress | Production SSL / HTTPS behavior and overall release readiness still require validation. |

---

## 3. RESOURCE EFFORT SUMMARY (PHASE 1 ONLY)

- **Original Allocation:** 13 MAN-DAYS
- **Consumed To Date:** 10 MAN-DAYS
- **Forecast Remaining:** 3 MAN-DAYS
- **Forecast Total:** 13 MAN-DAYS
- **Forecast Overrun:** 0 MAN-DAYS / 0%
- **Budget Status:** WITHIN BUDGET <!-- Options: WITHIN BUDGET | OVER BUDGET -->
- **Consumed Percentage:** 77%
- **Consumed Subtext:** 10 of 13 man-days consumed

---

## 4. WHAT CHANGED THIS WEEK?

### Completed Work
- Table Plan manual flow implemented using tools.
- Real-time seat-map-based element sizing implemented.
- Layout validation implemented.
- Seating and curve accuracy improvement progressed to approximately 50%.
- Additional external tools are being implemented.

### Enhancements
- Venue block detection accuracy improvements.
- 3D venue implementation started.
- Polling interval updated from 5 seconds to 30 seconds.
- Loading behavior improvements.
- Retry logic improvements are under development.

### Support / Development Setup
- Android development setup / HTTP-related fixes for SSL certificate issues.
- X-api-key header added.
- User entitlement GET fix applied.
- Additional supporting GET/service configuration fixes applied.

- **Material Notes:** No other material changes reported in this period.

---

## 5. RISKS / ISSUES & CEO ATTENTION

### Top Risks / Issues
| Priority | Risk / Issue Description | Severity |
| :---: | :--- | :---: |
| 1 | Production SSL / HTTPS validation is still required. | MEDIUM |
| 2 | Ticket timeout / retry behavior should be verified during UAT. | MEDIUM |
| 3 | Over-retry / HTTP service-limit behavior has not yet been validated in production. | HIGH |

### Decisions / Approvals Required
- Confirm production timeline and SSL hardening approach. | **Due:** N/A
- Complete final QA and UAT checks. | **Due:** N/A

### Escalation Status
- No critical escalations reported.

### Management Note
- Core development is complete.
- The remaining **3 man-days** are allocated for testing and bug fixing.

---

## 6. AT A GLANCE (PHASE 1 ONLY)

- **Overall Progress (Scope Complete):** 90%
- **Time Elapsed:** 69%
- **Effort Consumed:** 77%
- **Completed Items:** 5
- **Pending / Follow-Up Items:** 1
- **Enhancement Areas Completed:** 4
- **Key Insight Note:** Scope completion is at 90% with 77% of allocated effort consumed. The remaining focus is production validation, final QA, testing and bug fixing. Overall status remains AMBER due to outstanding production validation and release-readiness risks.

---

## REPORTING NOTES
This card summarizes Greyhound Dog Race Customer Mobile App progress for **17–28 August 2026**. Allocation-based figures are actual for this reporting period. Time elapsed is calculated against the original Phase 1 schedule from **17 August 2026 to 2 September 2026**.
