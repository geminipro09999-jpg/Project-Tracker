# WEEKLY PROJECT VISIBILITY CARD

> **Dev Team Instructions:** Fill out this markdown report every Friday. Do not remove table headers or field labels.

## PROJECT METADATA
- **Company:** Unicom TIC Incubator
- **Project ID:** TBD
- **Client:** TBD
- **Project Name:** ONEXSO HRMS
- **Current Release:** RELEASE 1
- **Week No:** WEEK 7
- **Week Ending Date:** 4 SEPTEMBER 2026
- **Overall Status:** AMBER

---

## RESOURCE ALLOCATION
- **Total Allocated Man-Days:** TBD
- **Release Start Date:** 17 JUL 2026

| Resource Name | Role | Allocation (Man-Days) | Main Responsibility |
| :--- | :--- | :---: | :--- |
| Thivaharan | Project Coordinator | TBD | Planning, coordination, reporting |
| Dapiyshanth | Team Lead | TBD | Technical leadership, development, integration |
| Kajaatharan | Developer | TBD | Development |
| Pirakeerthan | Developer | TBD | Development |

---

## 1. SCOPE & RELEASE JOURNEY

### Delivered Releases
- None yet - Release 1 is the first release and is currently in progress (not yet gone live)

### Current Release (RELEASE 1)

#### Core Modules

| Core Module | Main Scope / Objective | Current Status |
| --- | --- | --- |
| **Authentication & Security** | Secure login, MFA, tenant/admin authentication, authorization, host isolation, rate limiting and security controls | 🟢 Strong |
| **Tenant Management** | Tenant creation, activation, suspension, reactivation, cancellation and lifecycle management | 🟢 Strong |
| **Platform Administration** | Platform-level users, roles, subscription plans, invoices, modules, configurations, OAuth and service-key management | 🟢 Strong |
| **Roles & Permissions** | Role creation, permission assignment and module/action-level access control | 🟢 Strong |
| **Organization Administration** | Legal entities, departments, positions and reporting hierarchy management | 🟢 Strong |
| **Employee Management** | Employee onboarding, profile, personal information, emergency contacts, dependents, bank details and self-service | 🟢 Strong |
| **Onboarding & Offboarding** | Employee onboarding/offboarding workflows, checklists, task assignment, approvals and access revocation | 🟢 Strong |
| **Leave Management** | Leave types, policies, entitlements, requests, approvals, cancellation, balance audit, team calendar and year-end processing | 🟢 Complete |
| **Attendance** | Clock-in/out, breaks, attendance history, daily status and correction approval workflow | 🟢 Strong |
| **Calendar & Scheduling** | Month/Week/Day calendar, recurring events, invitations, RSVP, conflict detection and rescheduling | 🟢 Strong |
| **Work Management** | Projects, objectives, milestones, tasks, sprints and Kanban workflow | 🟡 In Progress |
| **Workforce Intelligence** | Activity monitoring, application usage, device state, productivity scoring, screenshots, identity verification and exception detection | 🟠 Early |
| **Billing & Subscription** | Plans, subscriptions, invoices, manual payment confirmation and Stripe webhook processing | 🟡 In Progress |

#### Integrations

| Integration | Purpose | Current Status |
| --- | --- | --- |
| **Stripe** | Subscription/payment processing and payment event handling | 🟡 Partial - webhooks only, no checkout/payment-initiation flow yet |
| **Google Calendar** | External calendar synchronization | 🔴 Not Implemented |
| **Microsoft Outlook Calendar** | External calendar synchronization | 🔴 Not Implemented |
| **Google (admin SSO)** | Platform admin login | 🟢 Implemented |
| **GitHub (tenant)** | Tenant-user OAuth connect/disconnect | 🟡 Partial - functional but narrow |
| **Microsoft / Zoom** | Platform-level OAuth config | 🟠 Config-only - no working tenant SSO/meeting flow yet |
| **Email Service - SendGrid / Resend** | Invitations, notifications and system emails | 🟢 Implemented |
| **Cloudflare R2** | File/object storage | 🟢 Implemented |
| **AWS Rekognition** | Identity verification / biometric liveness | 🟡 Partial - works for enrollment, no recurring/random verification |
| **Tray Monitoring Agent** | Workforce activity and device data collection | 🟢 Collectors wired and working end-to-end |

**Note:** Google/Outlook OAuth configuration exists, but actual calendar synchronization is **not implemented yet**.

#### Specific Objectives of Current Release

**Objective 1 - Multi-Tenant SaaS Foundation:** tenant isolation, tenant lifecycle, platform administration, role & permission framework, subscription/module entitlement structure

**Objective 2 - Core HR Management:** organization structure, employee management, onboarding/offboarding, leave management, attendance management, employee self-service

**Objective 3 - Centralized Workforce Scheduling:** company and individual calendar, recurring events, participant management, conflict detection, leave/training/review-related calendar events

**Objective 4 - Work Management:** projects, objectives and milestones, tasks, sprints, Kanban-based execution. Remaining gaps: time tracking, reporting, and some progress-calculation capabilities

**Objective 5 - Workforce Intelligence Foundation:** application/activity data collection, device-state information, productivity scoring, screenshots, identity verification, exception detection, wellness-related nudges - the product direction is "Work Context Intelligence" (connecting activity data with work context), not plain employee monitoring

**Objective 6 - Commercialization Foundation:** subscription plans, module entitlements, invoice management, payment event handling, Stripe integration foundation. Remaining: actual Stripe checkout/payment initiation and subscription lifecycle APIs

**Objective 7 - Production Readiness:** production cloud environment, domain configuration, SSL/HTTPS, deployment pipeline, monitoring/logging, security validation, performance validation, final UAT, release sign-off

**Executive summary:** The current release is focused on establishing ONEXSO's core SaaS, HR, workforce management and workforce intelligence foundations, while completing the remaining integrations, production-readiness activities and selected operational capabilities required for release.

### Future Releases
- **RELEASE 2 (candidate scope, pending confirmation)** - drawn from the current known gap list: Work Management time tracking, subtasks and Productivity Validation; Work Management/Organization reports & dashboards; Support Center backend; Stripe checkout/payment-collection flow; Google/Outlook calendar sync; Device Administration (asset inventory); data-privacy workflows (DSAR/retention); centralized audit trail; global search; System Control (maintenance mode/job control/release tracking)

---

## 2. CURRENT RELEASE PLAN (RELEASE 1 ONLY)

- **Original Plan Start:** 17 JUL 2026
- **Original Plan End:** 21 AUG 2026
- **Current Forecast Start:** 17 JUL 2026
- **Current Forecast End:** TBD
- **Schedule Delay:** TBD
- **Schedule Status:** ON TRACK

### Milestones Breakdown
| Milestone | Original Plan | Current Forecast | Variance | Status |
| :--- | :--- | :--- | :---: | :---: |
| Requirements Complete | 17 Jul 2026 | 17 Jul 2026 | 0 days | GREEN |
| Development Complete | 20 Jul 2026 | 20 Jul 2026 | 0 days | GREEN |
| System Test Complete | TBD | TBD | TBD | TBD |
| UAT Complete | 21 Jul 2026 | TBD | TBD | TBD |
| Go-Live | TBD | TBD | TBD | TBD |

---

## 3. RESOURCE EFFORT SUMMARY (RELEASE 1 ONLY)

- **Original Allocation:** TBD MAN-DAYS
- **Consumed To Date:** TBD MAN-DAYS
- **Forecast Remaining:** TBD MAN-DAYS
- **Forecast Total:** TBD MAN-DAYS
- **Forecast Overrun:** TBD
- **Budget Status:** TBD (WITHIN BUDGET / OVER BUDGET)
- **Consumed Percentage:** TBD
- **Consumed Subtext:** TBD

---

## 4. WHAT CHANGED THIS WEEK?

- **Delivered:** Leave Management reached full completion
- **Delivered:** Calendar module and redesigned Employee Dashboard shipped
- **Delivered:** Workforce Monitoring tray-app data collection now working end-to-end; monitoring screens mostly done
- **Fixed:** Dashboard reliability and data-accuracy issues resolved
- **Scope Change:** None this week
- **Effort Change:** None this week
- **Material Notes:** TBD

---

## 5. RISKS / ISSUES & CEO ATTENTION

### Top Risks / Issues
| Priority | Risk / Issue Description | Severity |
| :---: | :--- | :---: |
| 1 | Production infrastructure not started - domain, SSL, hosting, monitoring, and backup are all pending | HIGH |
| 2 | No production UAT has been performed yet | HIGH |
| 3 | Stripe checkout/payment-collection flow missing - billing can invoice but cannot self-serve collect payment yet | MEDIUM/HIGH |

### Decisions / Approvals Required
- **Approve domain name** for production deployment
- **Approve production database engine** (PostgreSQL or MySQL)

### Escalation Status
TBD

---

## 6. AT A GLANCE (RELEASE 1 ONLY)

- **Overall Progress (Scope Complete):** TBD (rough code-evidence audits exist internally; confirm a figure before publishing)
- **Time Elapsed:** TBD
- **Effort Consumed:** TBD
- **Key Insight Note:** TBD
