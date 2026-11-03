# 7. Scope & Estimation

Work Breakdown Structure by major feature. Complexity is Simple, Medium or Complex. Priority is Must (core, always delivered), Should (delivered if the schedule holds) or Could (first to be cut). Effort is a preliminary estimate in man-hours, to be confirmed with the team.

**Capacity check:** 5 members × 8 weeks × about 30 hours per week = 1,200 man-hours. The estimate is 802 man-hours (Must 566, Should 192, Could 44). The Must scope alone is under half of the capacity, and the whole estimate still fits at 25 hours per week (1,000 man-hours), leaving about 20-33% for rework, other courses and risk.

**8-week plan:**

- **Weeks 1-2:** Architecture, database, project setup, authentication and RBAC (FE1, FE2, 17.1).
- **Weeks 3-4:** Contest configuration, participant registration, film roll and photograph submission (FE3-FE7).
- **Weeks 5-6:** Submission verification, AI duplicate detection and judging with score ranking (FE8-FE11).
- **Week 7:** Results, archive, then Should features (mobile, AI keywording, analytics, notifications), plus integration testing.
- **Week 8:** Bug fixing, deployment, documentation and the final capstone report.

| No. | WBS Item | Complexity | Priority | Est. Effort (man-hours) |
| --- | --- | --- | --- | --- |
| 1 | **FE1. Account & Access Management** | | | **36** |
| 1.1 | Register, Login, Logout & Password Recovery (JWT) | Simple | Must | 12 |
| 1.2 | User Profile & Security (Change Pass) | Simple | Should | 8 |
| 1.3 | RBAC (Roles & Permissions Config) | Complex | Must | 16 |
| 2 | **FE2. System & Master Data Management** | | | **30** |
| 2.1 | System Settings Configuration | Simple | Must | 6 |
| 2.2 | Master Data Catalogs (Film Stock, Camera, Lens, Lab) | Medium | Must | 14 |
| 2.3 | Activity Log & Monitoring | Medium | Could | 10 |
| 3 | **FE3. Contest Planning & Configuration** | | | **44** |
| 3.1 | Contest Setup & Status Lifecycle | Medium | Must | 16 |
| 3.2 | Category & Regulation Management | Medium | Must | 12 |
| 3.3 | Award Structure Configuration | Simple | Must | 6 |
| 3.4 | Contest Templates | Medium | Could | 10 |
| 4 | **FE4. Judging Criteria Setup** | | | **16** |
| 4.1 | Criteria & Weight Configuration | Medium | Must | 12 |
| 4.2 | Film Photography Criteria Presets | Simple | Should | 4 |
| 5 | **FE5. Participant Profile & Registration** | | | **32** |
| 5.1 | Participant Profile & Portfolio | Simple | Must | 8 |
| 5.2 | Contest Browsing & Registration | Medium | Must | 14 |
| 5.3 | Registration Approval by Organizer | Simple | Must | 6 |
| 5.4 | Contest History | Simple | Could | 4 |
| 6 | **FE6. Film Roll & Frame Management** | | | **42** |
| 6.1 | Film Roll Management | Medium | Must | 14 |
| 6.2 | Frame Management & Linking to Submissions | Medium | Must | 14 |
| 6.3 | Film Roll & Frame Screens (Flutter) | Medium | Should | 14 |
| 7 | **FE7. Photograph Submission & Tracking** | | | **72** |
| 7.1 | Image Upload to Cloud Storage | Complex | Must | 16 |
| 7.2 | Submission Form with Technical Metadata | Complex | Must | 20 |
| 7.3 | Negative / Contact Sheet References | Simple | Should | 4 |
| 7.4 | Submission Tracking & Editing | Medium | Must | 12 |
| 7.5 | Submission Screens (Flutter) | Complex | Should | 20 |
| 8 | **FE8. Submission Verification** | | | **36** |
| 8.1 | Automated Rule Validation | Medium | Must | 16 |
| 8.2 | Organizer Review Workflow | Medium | Must | 14 |
| 8.3 | Flagged Submissions Queue | Simple | Should | 6 |
| 9 | **FE9. AI Image Verification** | | | **78** |
| 9.1 | Duplicate & Similar Image Detection | Complex | Must | 32 |
| 9.2 | AI-Generated Image Detection | Complex | Should | 36 |
| 9.3 | Flagging & Review Integration | Medium | Must | 10 |
| 10 | **FE10. Judge Assignment & Judging Workspace** | | | **72** |
| 10.1 | Judge Assignment | Medium | Must | 10 |
| 10.2 | Judge Workspace (Image Viewer & Metadata) | Medium | Must | 16 |
| 10.3 | Scoring & Comments | Complex | Must | 24 |
| 10.4 | Multi-Round Judging | Complex | Should | 18 |
| 10.5 | Final Result Confirmation | Simple | Must | 4 |
| 11 | **FE11. Score Aggregation & Ranking** | | | **22** |
| 11.1 | Score Aggregation & Ranking Logic | Complex | Must | 14 |
| 11.2 | Evaluation Record Keeping | Medium | Must | 8 |
| 12 | **FE12. Result Publication & Online Exhibition** | | | **30** |
| 12.1 | Result Publication | Medium | Must | 10 |
| 12.2 | Award Management | Simple | Must | 6 |
| 12.3 | Online Exhibition Page | Medium | Should | 14 |
| 13 | **FE13. Digital Archive** | | | **30** |
| 13.1 | Archive of Winning Works | Medium | Must | 10 |
| 13.2 | Archive Search & Browse | Medium | Should | 14 |
| 13.3 | Archive Detail Page | Simple | Must | 6 |
| 14 | **FE14. AI Keywording & Categorization** | | | **24** |
| 14.1 | Keyword Generation (OpenAI API) | Medium | Should | 14 |
| 14.2 | Category Suggestion & Manual Override | Medium | Could | 10 |
| 15 | **FE15. Contest Analytics & Reports** | | | **30** |
| 15.1 | Statistics Computation | Medium | Should | 12 |
| 15.2 | Dashboards & Charts | Medium | Should | 14 |
| 15.3 | Report Export | Simple | Could | 4 |
| 16 | **FE16. Notifications & Feedback** | | | **20** |
| 16.1 | Email Notifications | Medium | Should | 10 |
| 16.2 | In-App Notifications | Simple | Could | 6 |
| 16.3 | Results & Feedback Delivery | Simple | Should | 4 |
| 17 | **Project-Wide Activities** | | | **188** |
| 17.1 | Architecture, Database Design & Project Setup | Complex | Must | 24 |
| 17.2 | System Integration & Testing | Complex | Must | 70 |
| 17.3 | Cloud Deployment & Version Control Setup | Medium | Must | 14 |
| 17.4 | Technical Documentation & Capstone Report | Medium | Must | 30 |
| 17.5 | Project Management & Review Meetings | Simple | Must | 50 |
| | **Total** | | | **802** |
