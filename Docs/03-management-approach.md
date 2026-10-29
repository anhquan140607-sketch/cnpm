# Project Objectives, Risks and Management Approach

## 1.2 Project Objectives

Deliver all Must features (FE1-FE13) of the film photography contest platform within 8 weeks, with quality gates at every testing stage.

| # | Testing Stage | Test Coverage | No. of Defects | % of Defect | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 | Reviewing | 100% artifacts reviewed | - | - | Peer review of SRS, design and test cases |
| 2 | Unit Test | ≥70% coverage of core logic (scoring, validation, contest lifecycle) | 0 critical; ≤10 minor | ≤10% | Automated in the Git pipeline |
| 3 | Integration Test | ≥80% API/flow coverage | 0 critical; ≤10 minor | ≤8% | Postman/Swagger; AI and cloud storage calls |
| 4 | System Test | ≥90% of Must features | 0 critical; ≤5 minor | ≤5% | Staging environment regression |
| 5 | Acceptance Test | 100% of Core Flows 1-5 | 0 critical/blocker | 0% | UAT with supervisor and film photographers |

## 1.3 Project Risks

| # | Risk Description | Impact | Possibility | Response Plans |
| --- | --- | --- | --- | --- |
| 1 | Tight 8-week schedule; scope grows beyond capacity | High | High | Must/Should/Could priorities; cut Could, then Should first; review burndown every sprint |
| 2 | AI features inaccurate or hard to build (duplicate detection, AI-generated image detection) | High | Medium | Early proof of concept in Sprint 1-2; pretrained models/APIs; results as warnings with manual review; AI-generated detection is Should |
| 3 | Third-party services (OpenAI API, cloud storage, Firebase/Azure) are unstable, limited by quota or cost | Medium | Medium | Set up accounts early; retry and fallback to manual verification; monitor quota; use free tiers carefully |
| 4 | Limited film photography domain knowledge (metadata, judging criteria) | Medium | Medium | Consult a film photography club or photographers; prototype the metadata form early; get supervisor feedback |
| 5 | Changing or unclear requirements (e.g., blind judging, template rules) | Medium | Medium | Baseline the scope in Section 6; change control; supervisor sign-off at each sprint review |
| 6 | Team member availability or skill gaps (Flutter, AI, cloud) | Medium | Medium | Backup owner per module; short daily stand-ups; knowledge sharing; effort buffer of 20-33% |
| 7 | Data privacy and security (accounts, uploaded images) | High | Low | JWT with RBAC; private cloud storage with access control; audit logs; no public image links before results |
| 8 | Performance under large image uploads and concurrent judging | Medium | Low | Image compression and thumbnails; pagination; caching; load test in Sprint 4 |

## 2. Management Approach

### 2.1 Project Process

- **Methodology:** Agile Scrum with 2-week sprints, 4 sprints in total (8 weeks).
- **Phases:**
  - **Sprint 1 (Weeks 1-2):** Requirements, architecture and database design, project setup, authentication and RBAC, system and master data (FE1, FE2), AI proof of concept.
  - **Sprint 2 (Weeks 3-4):** Contest configuration, participant registration, film roll and frame management, photograph submission (FE3-FE7).
  - **Sprint 3 (Weeks 5-6):** Submission verification, AI image verification, judging, score aggregation and ranking (FE8-FE11).
  - **Sprint 4 (Weeks 7-8):** Results, exhibition and archive (FE12-FE13), Should features (FE14-FE16, Flutter screens), system testing, UAT, deployment and the capstone report.
- **Roles (to confirm):** Supervisor as Product Owner, one member as Scrum Master and Git maintainer, the other four as developers.
- **Scrum ceremonies:** Daily stand-up (15 minutes), Sprint Planning, Sprint Review with the supervisor, Sprint Retrospective.
- **Artifacts:** Product Backlog, Sprint Backlog, Burndown Chart, Increment.
- **Jira setup:**
  - Scrum board with one Epic per feature (FE1-FE16) and one Epic for Project-Wide Activities.
  - Each WBS item in [02-scope-estimation.md](02-scope-estimation.md) is a Story or Task, using its man-hours as the original estimate and its priority (Must/Should/Could) as a label.
  - Defects are Bug issues with severity (critical, major, minor).
  - Workflow: To Do → In Progress → In Review → Testing → Done.
  - Every sprint backlog is filled with Must items first.
- **Source control:** Git with a protected main branch where only the maintainer merges, one feature branch per Jira issue key, and commit messages that include the key. Sprint milestones and release tags (e.g., v0.1) mark each increment. See [04-git-workflow-guide.md](04-git-workflow-guide.md).

### 2.2 Quality Management

The quality objective is a stable, accurate and maintainable system that completes all five Core Flows. The approach includes:

- **Defect Prevention:** Enforce coding standards with linting, normalize the database with constraints and indexes, validate all inputs, and use a Definition of Done for every Jira issue.
- **Reviewing:** Mandatory code review by at least one other member before merging, and two reviewers for critical modules (authentication, scoring). Peer review of SRS, design documents and test cases.
- **Unit Testing:**
  - Tools: Jest for the web frontend, xUnit or Jest for the backend (depending on the chosen stack), flutter_test for mobile.
  - Goal: ≥70% coverage of core logic such as score aggregation, submission validation and contest status rules.
- **Integration Testing:**
  - Tools: Postman and Swagger for API and workflow testing.
  - Covers JWT and RBAC checks, cloud storage upload, and AI calls (OpenAI API, image similarity), with mocks and the manual-review fallback when a service is down.
- **System Testing:**
  - Conducted on a staging environment on Azure or Firebase.
  - Full regression of all Must features (FE1-FE13).
  - Load testing (e.g., JMeter or k6) for concurrent judging and image uploads.
- **Acceptance Testing:**
  - User Acceptance Testing (UAT) with the supervisor and film photographers acting as organizers, judges and participants.
  - Ensure 100% of the Core Flows 1-5 pass before the final demo.
- **Defect Management:** Bugs are logged in Jira and fixed by severity: critical and blocker issues before any new feature work.
