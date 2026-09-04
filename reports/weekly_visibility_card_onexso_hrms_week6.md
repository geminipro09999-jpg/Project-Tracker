# WEEKLY PROJECT VISIBILITY CARD

> **Dev Team Instructions:** Fill out this markdown report every Friday. Do not remove table headers or field labels.

## PROJECT METADATA
- **Company:** Unicom TIC Incubator
- **Project ID:** ONEXSO_HRMS
- **Client:** Internal Product
- **Project Name:** ONEXSO HRMS
- **Current Release:** RELEASE 1
- **Week No:** WEEK 6
- **Week Ending Date:** 28 AUGUST 2026
- **Overall Status:** AMBER

---

## RESOURCE ALLOCATION
- **Total Allocated Man-Days:** 160
- **Release Start Date:** 17 JUL 2026

| Resource Name | Role | Allocation (Man-Days) | Main Responsibility |
| :--- | :--- | :---: | :--- |
| Thivaharan | Project Coordinator | 40 | Planning, coordination, reporting |
| Dapiyshanth | Team Lead | 50 | Technical leadership, development, integration |
| Kajaatharan | Developer | 35 | Development |
| Pirakeerthan | Developer | 35 | Development |

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
| **Employee Management** | Employee onboarding, profile, personal information, emergency contacts, dependents, bank details and self-service | 🟡 In Progress |
| **Onboarding & Offboarding** | Employee onboarding/offboarding workflows, checklists, task assignment, approvals and access revocation | 🟢 Strong |
| **Leave Management** | Leave types, policies, entitlements, requests, approvals, cancellation, balance audit, team calendar and year-end processing | 🟡 In Progress |
| **Attendance** | Clock-in/out, breaks, attendance history, daily status and correction approval workflow | 🟢 Strong |
| **Calendar & Scheduling** | Month/Week/Day calendar, recurring events, invitations, RSVP, conflict detection and rescheduling | 🟡 In Progress |
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
| **Tray Monitoring Agent** | Workforce activity and device data collection | 🟠 Device authorization/activation groundwork in progress |

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
- **Current Forecast End:** 04 SEP 2026
- **Schedule Delay:** +14 DAYS
- **Schedule Status:** DELAYED

### Milestones Breakdown
| Milestone | Original Plan | Current Forecast | Variance | Status |
| :--- | :--- | :--- | :---: | :---: |
| Requirements Complete | 17 Jul 2026 | 17 Jul 2026 | 0 days | GREEN |
| Development Complete | 20 Jul 2026 | 20 Jul 2026 | 0 days | GREEN |
| System Test Complete | 14 Aug 2026 | 21 Aug 2026 | +7 days | AMBER |
| UAT Complete | 21 Aug 2026 | 28 Aug 2026 | +7 days | AMBER |
| Go-Live | 21 Aug 2026 | 04 Sep 2026 | +14 days | RED |

---

## 3. RESOURCE EFFORT SUMMARY (RELEASE 1 ONLY)

- **Original Allocation:** 160 MAN-DAYS
- **Consumed To Date:** 112 MAN-DAYS
- **Forecast Remaining:** 48 MAN-DAYS
- **Forecast Total:** 160 MAN-DAYS
- **Forecast Overrun:** 0 MAN-DAYS
- **Budget Status:** WITHIN BUDGET
- **Consumed Percentage:** 70%
- **Consumed Subtext:** 112/160 MAN-DAYS

---

## 4. WHAT CHANGED THIS WEEK?

- **Delivered:** Leave Management continued (policies, entitlements, requests/approvals build-out)
- **Delivered:** Employee Management foundation work progressed (multiple merges)
- **Delivered:** Work Management project/objective tree rewritten; approval-hours and component tuning shipped
- **Delivered:** Attendance & Leave Management frontend integration
- **Delivered:** Tray device authorization / activation groundwork shipped (backend + frontend)
- **Fixed:** Tenant creation RLS admin-mode issue resolved
- **Scope Change:** None this week
- **Effort Change:** None this week
- **Material Notes:** Week 6 focus on core HR & Leave management workflows.

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
Production infrastructure setup requires immediate domain and cloud environment decision.

---

## 6. AT A GLANCE (RELEASE 1 ONLY)

- **Overall Progress (Scope Complete):** 75%
- **Time Elapsed:** 70%
- **Effort Consumed:** 70%
- **Key Insight Note:** Core SaaS & HR modules are strong; production infra, UAT, and Stripe self-serve payment flows are critical pending items.
