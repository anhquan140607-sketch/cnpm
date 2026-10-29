# Software Requirements Specification (SRS)

**Project:** AI-powered Film Photography Contest Management Platform
**Vietnamese:** Nền tảng tổ chức và quản lý cuộc thi nhiếp ảnh phim tích hợp trí tuệ nhân tạo
**Version:** 1.0 (draft for team and supervisor review)
**Team:** 5 members, 8 weeks, Agile Scrum (4 sprints)

Conventions used in this document:

- **shall** marks a mandatory requirement.
- **Priority** is Must, Should or Could, using the same meaning as in [02-scope-estimation.md](02-scope-estimation.md): Must is always delivered, Should is delivered if the schedule holds, Could is cut first.
- **WBS** gives the work item in [02-scope-estimation.md](02-scope-estimation.md) whose effort covers the requirement.
- **(derived)** marks a detail inferred from the project proposal and not stated word for word in it. Derived details need confirmation by the team or supervisor.

---

## 1. Introduction

### 1.1 Purpose

This document specifies the functional and non-functional requirements of the AI-powered Film Photography Contest Management Platform. It is the agreed basis for design, implementation, testing and acceptance, and it expands the 16 major features (FE1-FE16) in [01-project-scope.md](01-project-scope.md).

### 1.2 Background and problem statement

Film photography is growing again, and film photography contests help preserve analog culture and connect photographers. A film contest must manage more than image files. Each photograph has technical information: film stock, camera, lens, film format, development laboratory, scanning process and sometimes negative or contact-sheet references.

Today many contests are run with separate online forms, spreadsheets, email, cloud storage and social media. This increases administrative work, makes submission verification and judging difficult, and limits long-term management of contest data. Participants also have no central place for their contest history and film photography portfolio.

### 1.3 Product scope

The product is a web and mobile platform that supports the full life cycle of a film photography contest: planning and configuration, participant registration, film submission with metadata, submission verification, judging, result publication and digital archiving. Artificial Intelligence assists organizers by detecting duplicate or highly similar images, identifying AI-generated images, generating keywords and categories, and producing analytics.

Excluded from scope (see LI1-LI21 in [01-project-scope.md](01-project-scope.md)): online payment, physical logistics, social features, offline mode, integration with external systems, custom AI model training, and automatic reading of film edge codes.

### 1.4 Definitions and abbreviations

| Term | Meaning |
| --- | --- |
| Film roll | One roll of film used by a participant, with its film and camera information |
| Frame | A single exposure on a film roll, identified by a frame number |
| Submission | A scanned photograph entered in a contest category, linked to a frame and its technical metadata |
| Metadata | Technical information of a photograph: film brand and stock, ISO, film format, camera, lens, frame number, shooting location, developing lab, scanning specifications, optional negative or contact-sheet reference |
| Master data | Reference catalogs managed by the administrator (film brands and stocks, ISO values, formats, cameras, lenses, labs, scanners) |
| Core Flow | One of the five business flows of the proposal (Section 3) |
| RBAC | Role-based access control |
| JWT | JSON Web Token, used for authentication |
| UAT | User acceptance testing |
| FE / FR / NFR / LI | Major feature / functional requirement / non-functional requirement / limitation or exclusion |

### 1.5 References

- Project proposal: "AI-powered Film Photography Contest Management Platform" (đề tài).
- [01-project-scope.md](01-project-scope.md): major features and limitations.
- [02-scope-estimation.md](02-scope-estimation.md): WBS, priority and effort.
- [03-management-approach.md](03-management-approach.md): objectives, risks, process and quality management.

### 1.6 Document overview

Section 2 describes the product and its users. Section 3 describes the five Core Flows. Section 4 lists the functional requirements by feature. Section 5 lists data, external interface and non-functional requirements. Section 6 gives acceptance criteria. The appendices give a traceability matrix and open issues.

---

## 2. Overall Description

### 2.1 Product perspective

The product is a new, standalone system with three client applications and one backend:

- A **web portal** for administrators, organizers, judges and participants (ReactJS / Next.js).
- A **mobile application** for participants to register and submit film photographs (Flutter).
- A **backend API** (ASP.NET Core Web API or Node.js with Express) with a relational database (PostgreSQL or MySQL).
- An **AI module** using Computer Vision, the OpenAI API and image similarity detection.
- **Cloud storage** for images and digital assets (Firebase Storage or Azure Blob Storage), deployed on Microsoft Azure or Firebase.

The backend technology and the database are chosen once during the design phase.

### 2.2 Product functions

| Feature | Summary |
| --- | --- |
| FE1 Account & Access Management | Registration, login, password recovery, profile and role-based access |
| FE2 System & Master Data Management | System settings, film master data, activity log |
| FE3 Contest Planning & Configuration | Contests, categories, regulations, awards, templates |
| FE4 Judging Criteria Setup | Weighted film-specific scoring criteria |
| FE5 Participant Profile & Registration | Participant profile, contest browsing, registration and approval |
| FE6 Film Roll & Frame Management | Film rolls and frames linked to submissions |
| FE7 Photograph Submission & Tracking | Upload with metadata and status tracking |
| FE8 Submission Verification | Automatic checks and organizer review |
| FE9 AI Image Verification | Duplicate and AI-generated image detection with manual review |
| FE10 Judge Assignment & Judging Workspace | Assignment, scoring, comments, multiple rounds, confirmation |
| FE11 Score Aggregation & Ranking | Aggregation, ranking and evaluation records |
| FE12 Result Publication & Online Exhibition | Rankings, results, awards and online exhibition |
| FE13 Digital Archive | Archive of award-winning works with metadata |
| FE14 AI Keywording & Categorization | Generated keywords and suggested categories |
| FE15 Contest Analytics & Reports | Statistics, dashboards and reports |
| FE16 Notifications & Feedback (derived) | Result, feedback and status notifications |

### 2.3 User classes and roles

| Role | Description | Main responsibilities |
| --- | --- | --- |
| Administrator | Operates the platform | Manage users and access permissions, configure system settings, manage master data, monitor platform activities, maintain contest configurations |
| Contest Organizer | Runs contests | Create and configure contests, define categories and judging criteria, manage registrations, verify submissions, assign judges, publish results, manage awards and online exhibitions |
| Judge | Evaluates photographs | Review assigned submissions, evaluate by contest criteria, provide comments and scores, take part in multiple judging rounds, confirm final results |
| Participant (Film Photographer) | Enters photographs | Manage personal profile, register for contests, submit photographs, maintain film roll and frame information, track submission status, receive results and feedback |

The AI module is a system component, not a user. It supports the organizer and never makes a final decision.

### 2.4 Operating environment

- Web portal on current desktop and mobile browsers.
- Participant mobile application on Android and iOS through Flutter.
- Backend and database hosted on Microsoft Azure or Firebase; source code in GitHub.

### 2.5 Design and implementation constraints

- Authentication shall use JWT with role-based access control.
- Images and digital assets shall be stored on cloud storage.
- The architecture shall be modular for scalability and maintenance.
- The platform shall support multiple simultaneous contests and concurrent judging.
- Pretrained models and APIs are used for AI; no custom model training (LI8).
- Only the participant functions of FE5, FE6 and FE7 have a mobile version (LI21).
- Project resources are 5 members and 8 weeks, so Should and Could features are built only if time allows (LI20).

### 2.6 Assumptions and dependencies

- Organizers, judges and participants have internet access; there is no offline mode (LI5).
- Scanned images are provided by participants in the formats allowed by the system settings.
- AI features depend on third-party services whose availability, quota and cost are outside the project's control (LI16). When a service is unavailable, verification falls back to manual review.
- Authenticity of film origin relies on declared metadata and organizer review, not on technical proof (LI12).

---

## 3. Business Core Flows

| Flow | Name | Description | Features |
| --- | --- | --- | --- |
| 1 | Contest Planning and Configuration | Organizers create contests by defining themes, categories, submission periods, judging schedules, evaluation criteria, award structures and regulations. Reusable templates simplify recurring contests while each event can have different rules. | FE3, FE4 |
| 2 | Film Submission and Metadata Management | Participants upload scanned photographs together with film brand, film stock, ISO, camera, lens, frame number, shooting location, developing lab and scanning specifications. The platform keeps the relationship between film rolls, frames and contest submissions. | FE6, FE7 |
| 3 | Submission Verification | Before judging, the platform checks file format, image quality, deadline and completeness of technical information. AI-assisted verification identifies duplicate images, detects AI-generated content and flags suspicious submissions for manual review by organizers. | FE8, FE9 |
| 4 | Judging and Evaluation Management | Organizers assign judges by category or round. Judges evaluate with configurable criteria (artistic creativity, composition, storytelling, technical execution, film grain, tonal range, color rendering, scan quality). The platform aggregates scores, ranks submissions and preserves evaluation records for transparency. | FE4, FE10, FE11 |
| 5 | Result Publication and Digital Archive | After judging, the platform calculates final rankings and publishes official results. Award-winning photographs are preserved in a digital archive with technical metadata, judging comments, contest information and historical records. | FE12, FE13 |

Supporting features used by all flows: FE1, FE2, FE5, FE14, FE15, FE16.

---

## 4. Functional Requirements

### 4.1 FE1. Account & Access Management

| ID | Requirement | Priority | WBS |
| --- | --- | --- | --- |
| FR-1.1 | The system shall allow a participant to register an account with email and password. Organizer, judge and administrator accounts shall be created or assigned by an administrator (derived). | Must | 1.1 |
| FR-1.2 | The system shall allow users to log in and log out. A successful login shall issue a JWT with an expiry time; invalid credentials shall be rejected with a clear message. | Must | 1.1 |
| FR-1.3 | The system shall allow a user to recover a forgotten password through a time-limited link sent by email. | Must | 1.1 |
| FR-1.4 | The system shall allow a logged-in user to view and edit basic profile information and change the password. | Should | 1.2 |
| FR-1.5 | The system shall enforce role-based access control for the four roles on every screen and API call. A request outside the user's role shall be denied. | Must | 1.3 |
| FR-1.6 | An administrator shall be able to create, update and deactivate user accounts, assign roles, and configure roles and permissions. | Must | 1.3 |

### 4.2 FE2. System & Master Data Management

| ID | Requirement | Priority | WBS |
| --- | --- | --- | --- |
| FR-2.1 | An administrator shall be able to configure system settings: allowed image formats, maximum upload size, minimum image quality and notification settings. | Must | 2.1 |
| FR-2.2 | An administrator shall be able to create, edit and deactivate master data: film brands and stocks, ISO values, film formats, cameras, lenses, developing laboratories and scanners. Data in use shall be deactivated, not deleted. | Must | 2.2 |
| FR-2.3 | The system shall record platform activities (logins, submissions, judging actions, configuration changes) with user, action and time, and let an administrator search and filter the log. | Could | 2.3 |

### 4.3 FE3. Contest Planning & Configuration

| ID | Requirement | Priority | WBS |
| --- | --- | --- | --- |
| FR-3.1 | An organizer shall be able to create and edit a contest with theme, description, regulations, submission period and judging schedule. | Must | 3.1 |
| FR-3.2 | A contest shall follow the status life cycle draft → open → closed → judging → published → archived. Submissions shall be accepted only while the contest is open. (derived) | Must | 3.1 |
| FR-3.3 | An administrator shall be able to view any contest configuration and lock or unlock it when a configuration problem must be corrected. | Must | 3.1 |
| FR-3.4 | An organizer shall be able to define contest categories and per-category submission rules, such as the maximum number of photographs per participant. | Must | 3.2 |
| FR-3.5 | The system shall show the contest regulations to participants before registration and submission. | Must | 3.2 |
| FR-3.6 | An organizer shall be able to define the award structure of each category, including ranks and special awards. | Must | 3.3 |
| FR-3.7 | An organizer shall be able to save a contest configuration as a template and create a new contest from it, with the ability to change any rule for the new event. | Could | 3.4 |

### 4.4 FE4. Judging Criteria Setup

| ID | Requirement | Priority | WBS |
| --- | --- | --- | --- |
| FR-4.1 | An organizer shall be able to configure scoring criteria for a contest or category, each with name, description, weight and maximum score. The weights shall add up to 100%. | Must | 4.1 |
| FR-4.2 | The system shall provide film photography criteria presets: artistic creativity, composition, storytelling, technical execution, film grain, tonal range, color rendering and scan quality. The organizer shall be able to select and edit them. | Should | 4.2 |
| FR-4.3 | Criteria shall be locked once judging starts so that all judges score by the same rules. (derived) | Must | 4.1 |

### 4.5 FE5. Participant Profile & Registration

| ID | Requirement | Priority | WBS |
| --- | --- | --- | --- |
| FR-5.1 | A participant shall be able to create and update a personal profile and view a portfolio of their own submitted photographs. | Must | 5.1 |
| FR-5.2 | A participant shall be able to browse open contests and view their details, categories and regulations. | Must | 5.2 |
| FR-5.3 | A participant shall be able to register for a contest and category. The system shall prevent duplicate registration and registration after the deadline. | Must | 5.2 |
| FR-5.4 | An organizer shall be able to view registrations and approve or reject each one, with a reason for rejection. | Must | 5.3 |
| FR-5.5 | A participant shall be able to view the history of contests they took part in and the results. | Could | 5.4 |

### 4.6 FE6. Film Roll & Frame Management

| ID | Requirement | Priority | WBS |
| --- | --- | --- | --- |
| FR-6.1 | A participant shall be able to create, edit and delete a film roll recording film brand, film stock, ISO, film format, camera, lens, developing laboratory and scanning specifications, choosing values from master data. | Must | 6.1 |
| FR-6.2 | A participant shall be able to add frames to a roll with frame number and shooting location. The frame number shall be unique within the roll. | Must | 6.2 |
| FR-6.3 | The system shall maintain the relationship film roll → frame → submission. A roll or frame linked to a submitted entry shall not be deletable. | Must | 6.2 |
| FR-6.4 | The participant mobile application shall provide the film roll and frame screens of FR-6.1 and FR-6.2. | Should | 6.3 |

### 4.7 FE7. Photograph Submission & Tracking

| ID | Requirement | Priority | WBS |
| --- | --- | --- | --- |
| FR-7.1 | A participant shall be able to upload a scanned photograph to cloud storage, with upload progress and a generated thumbnail. Files outside the allowed format or size shall be rejected. | Must | 7.1 |
| FR-7.2 | A participant shall be able to create a submission by selecting a contest category and a frame, entering title and description. The technical metadata of the linked roll and frame shall fill in automatically and mandatory fields shall be validated. | Must | 7.2 |
| FR-7.3 | The system shall enforce the per-category limit on the number of photographs and the submission period. | Must | 7.2 |
| FR-7.4 | A participant shall be able to attach an optional negative or contact-sheet reference to a submission. The reference is stored, not read automatically (LI9). | Should | 7.3 |
| FR-7.5 | A participant shall be able to track the status of each submission (submitted, under verification, accepted, rejected, needs revision), and edit or withdraw it before the submission deadline. | Must | 7.4 |
| FR-7.6 | The participant mobile application shall provide the submission screens of FR-7.1 to FR-7.5. | Should | 7.5 |

### 4.8 FE8. Submission Verification

| ID | Requirement | Priority | WBS |
| --- | --- | --- | --- |
| FR-8.1 | The system shall automatically check each submission for file format, image quality, submission deadline and completeness of technical information, and record the result with reasons. | Must | 8.1 |
| FR-8.2 | An organizer shall be able to open a submission with its image and metadata and approve it, reject it with a reason, or request revision. | Must | 8.2 |
| FR-8.3 | Only accepted submissions shall be available to judges. | Must | 8.2 |
| FR-8.4 | The system shall give organizers a queue of flagged submissions with the flag reasons. | Should | 8.3 |

### 4.9 FE9. AI Image Verification

| ID | Requirement | Priority | WBS |
| --- | --- | --- | --- |
| FR-9.1 | The system shall compare each new image with the images held on the platform (current contest and archive) using image similarity, and flag duplicates or highly similar images with a similarity score and the matched image. The comparison does not cover the wider internet (LI14). | Must | 9.1 |
| FR-9.2 | The system shall estimate the likelihood that an image is AI-generated and flag images above a configurable threshold. The result is a warning, not proof (LI13). | Should | 9.2 |
| FR-9.3 | The AI module shall never reject a submission by itself. Flagged submissions shall go to the organizer for manual review, and the organizer's decision shall be recorded. | Must | 9.3 |
| FR-9.4 | If an AI service is unavailable, the submission shall be marked "AI check pending" and manual verification shall continue (LI16). | Must | 9.3 |

### 4.10 FE10. Judge Assignment & Judging Workspace

| ID | Requirement | Priority | WBS |
| --- | --- | --- | --- |
| FR-10.1 | An organizer shall be able to assign judges to categories or judging rounds. A judge shall see only the submissions assigned to them. | Must | 10.1 |
| FR-10.2 | A judge shall have a dedicated workspace listing assigned submissions with zoomable image, film metadata and scoring progress. | Must | 10.2 |
| FR-10.3 | A judge shall be able to score each photograph for each configured criterion and add a comment. Drafts shall be saved and scores shall be editable until the round is closed. | Must | 10.3 |
| FR-10.4 | An organizer shall be able to configure several judging rounds (for example shortlist and final) and select the submissions that advance. | Should | 10.4 |
| FR-10.5 | A judge shall be able to confirm their final evaluation results. Confirmed scores shall be locked. | Must | 10.5 |

### 4.11 FE11. Score Aggregation & Ranking

| ID | Requirement | Priority | WBS |
| --- | --- | --- | --- |
| FR-11.1 | The system shall aggregate scores automatically, applying criteria weights and combining the scores of all judges, and rank submissions. The tie-breaking rule shall be defined by the organizer (derived). | Must | 11.1 |
| FR-11.2 | The system shall preserve detailed evaluation records (judge, criterion, score, comment, time) for transparency. Confirmed records shall not be changed. | Must | 11.2 |

### 4.12 FE12. Result Publication & Online Exhibition

| ID | Requirement | Priority | WBS |
| --- | --- | --- | --- |
| FR-12.1 | After all judges confirm, the system shall calculate final rankings. An organizer shall review and publish the official results, moving the contest to the published status. | Must | 12.1 |
| FR-12.2 | An organizer shall be able to record awards for winning submissions according to the award structure. | Must | 12.2 |
| FR-12.3 | An organizer shall be able to publish an online exhibition of award-winning works showing the photographer, title and technical information. | Should | 12.3 |

### 4.13 FE13. Digital Archive

| ID | Requirement | Priority | WBS |
| --- | --- | --- | --- |
| FR-13.1 | The system shall store award-winning photographs in the digital archive together with technical metadata, judging comments, contest information and history. Only award-winning works are archived by default (LI11). | Must | 13.1 |
| FR-13.2 | Users shall be able to browse and search the archive by contest, year, category, film stock, camera and keyword. | Should | 13.2 |
| FR-13.3 | The system shall provide a detail page for each archived work. | Must | 13.3 |

### 4.14 FE14. AI Keywording & Categorization

| ID | Requirement | Priority | WBS |
| --- | --- | --- | --- |
| FR-14.1 | The system shall generate keywords for a photograph using the OpenAI API, automatically on submission or on request. | Should | 14.1 |
| FR-14.2 | The system shall suggest a category for a photograph. Keywords and categories are suggestions only; an organizer shall be able to accept, edit or override them. | Could | 14.2 |

### 4.15 FE15. Contest Analytics & Reports

| ID | Requirement | Priority | WBS |
| --- | --- | --- | --- |
| FR-15.1 | The system shall compute statistics for a contest: registrations, submissions per category, flagged cases, and score distribution. | Should | 15.1 |
| FR-15.2 | The system shall show the statistics on a dashboard with charts and filters. | Should | 15.2 |
| FR-15.3 | An organizer shall be able to export a contest report (for example PDF or CSV). | Could | 15.3 |

### 4.16 FE16. Notifications & Feedback (derived)

| ID | Requirement | Priority | WBS |
| --- | --- | --- | --- |
| FR-16.1 | The system shall send email notifications for registration decisions, submission status changes and published results. | Should | 16.1 |
| FR-16.2 | The system shall show in-app notifications for the same events. | Could | 16.2 |
| FR-16.3 | After publication, participants shall be able to see their results and the judges' feedback on their submissions. | Should | 16.3 |

---

## 5. Data, Interface and Non-Functional Requirements

### 5.1 Logical data requirements

| Entity | Key attributes | Relationships |
| --- | --- | --- |
| User | name, email, password hash, role, status | has one role; owns film rolls, registrations, submissions |
| Contest | title, theme, description, regulations, periods, status | has many categories, criteria, registrations, rounds |
| Category | name, submission rules, award structure | belongs to a contest |
| Criterion | name, description, weight, max score | belongs to a contest or category |
| Registration | participant, contest, category, status, reason | links a participant and a contest |
| Film roll | film brand, film stock, ISO, film format, camera, lens, lab, scanning specs | belongs to a participant; has many frames |
| Frame | frame number, shooting location | belongs to a roll; may be linked to submissions |
| Submission | title, description, image reference, negative or contact-sheet reference, status, keywords | links a frame and a category; has AI check results |
| AI check result | type (duplicate, AI-generated), score, matched image, decision | belongs to a submission |
| Judge assignment | judge, category, round | links a judge and a category or round |
| Evaluation | judge, submission, criterion scores, comment, time, confirmed flag | links a judge and a submission |
| Award | rank or title, submission | belongs to a contest category |
| Archive item | submission snapshot, metadata, judging comments | created from an award-winning submission |
| Master data | type, value, status | referenced by film rolls |
| Activity log | user, action, time | written by all modules |

The relationship **film roll → frame → submission** shall be kept consistent at all times.

### 5.2 External interface requirements

| Interface | Requirement |
| --- | --- |
| User interface | Web portal responsive for desktop and mobile browsers; Flutter application for participants. Screens are role-specific. |
| Backend API | REST API over HTTPS, secured with JWT and documented with Swagger. |
| Cloud storage | Firebase Storage or Azure Blob Storage for images and thumbnails, private by default. |
| AI services | OpenAI API for keywords and categories; Computer Vision and image similarity detection for duplicate and AI-generated image checks. |
| Email service | An email sending service for notifications and password recovery (derived). |
| Source control | GitHub for code and documents; Jira for backlog and sprints. |

### 5.3 Non-functional requirements

| ID | Category | Requirement |
| --- | --- | --- |
| NFR-1 | Authentication and authorization | Authentication and authorization shall use JWT with role-based access control. Passwords shall be stored hashed. |
| NFR-2 | Storage | Images and digital assets shall be stored securely on cloud storage. Image access shall be controlled, and images shall not be publicly accessible before results are published (derived). |
| NFR-3 | Architecture | The software shall follow a modular design to facilitate scalability and maintenance. |
| NFR-4 | Concurrency | The platform shall support multiple simultaneous contests and concurrent judging activities. |
| NFR-5 | Performance (derived target) | Common pages shall load within 3 seconds under normal load; large images shall be shown as thumbnails with the full image loaded on demand. Targets are for capstone scale (LI17) and to be confirmed. |
| NFR-6 | Reliability | When an AI or cloud service fails, the system shall keep working and fall back to manual verification, with the failure recorded. |
| NFR-7 | Integrity and audit | Confirmed evaluations and published results shall not be modified. Important actions shall be recorded in the activity log. |
| NFR-8 | Usability | A participant shall be able to submit a photograph with its metadata without training, guided by form validation and clear messages. |
| NFR-9 | Maintainability | Code shall follow agreed coding standards and be reviewed before merging. Core logic (scoring, validation, contest status rules) shall have at least 70% unit test coverage. |
| NFR-10 | Compatibility | The web portal shall work on current versions of the major browsers; the mobile application on current Android and iOS versions. |

### 5.4 Constraints and exclusions

All limitations and exclusions LI1-LI21 in [01-project-scope.md](01-project-scope.md) apply to this specification. In particular: AI supports and does not replace judges (LI7); AI results are probabilistic (LI13); duplicate checks cover only images on the platform (LI14); and security follows the stated requirements without formal certification (LI17).

---

## 6. Acceptance Criteria

The system is accepted when all Core Flows 1-5 pass user acceptance testing and the Must requirements pass system testing, as defined in [03-management-approach.md](03-management-approach.md).

| Flow | Acceptance criteria |
| --- | --- |
| 1. Contest Planning and Configuration | An organizer can create a contest with categories, regulations, submission period, judging schedule, criteria and awards, and open it. A template can be reused with changed rules (if the Could requirement is built). The contest follows the defined status life cycle. |
| 2. Film Submission and Metadata Management | A registered participant can create a film roll and frames, upload a scanned photograph, and submit it with complete technical information. The submission shows the correct roll and frame, and the status can be tracked. Incomplete or invalid submissions are rejected with clear messages. |
| 3. Submission Verification | The system checks format, quality, deadline and completeness automatically. A duplicate image is flagged with its matched image. Flagged submissions reach the organizer, who can approve, reject or request revision. A failed AI service does not stop verification. |
| 4. Judging and Evaluation Management | An organizer assigns judges. A judge sees only assigned submissions, scores by every criterion, comments, and confirms the results. Scores are aggregated with the configured weights and submissions are ranked. Evaluation records are kept and cannot be changed after confirmation. |
| 5. Result Publication and Digital Archive | An organizer publishes official results and awards. Winning works appear in the digital archive with metadata and judging comments. Participants can see their results and feedback. |

Non-functional acceptance: the role restrictions of FR-1.5 hold for every role, and concurrent judging by several judges in several contests works without data loss.

---

## Appendix A. Traceability Matrix

| Feature | Core Flow | Roles | Requirements | WBS | Must / Should / Could requirements |
| --- | --- | --- | --- | --- | --- |
| FE1 | All | All | FR-1.1 to FR-1.6 | 1.1-1.3 | 5 / 1 / 0 |
| FE2 | All | Administrator | FR-2.1 to FR-2.3 | 2.1-2.3 | 2 / 0 / 1 |
| FE3 | 1 | Organizer, Administrator | FR-3.1 to FR-3.7 | 3.1-3.4 | 6 / 0 / 1 |
| FE4 | 1, 4 | Organizer | FR-4.1 to FR-4.3 | 4.1-4.2 | 2 / 1 / 0 |
| FE5 | Registration | Participant, Organizer | FR-5.1 to FR-5.5 | 5.1-5.4 | 4 / 0 / 1 |
| FE6 | 2 | Participant | FR-6.1 to FR-6.4 | 6.1-6.3 | 3 / 1 / 0 |
| FE7 | 2 | Participant | FR-7.1 to FR-7.6 | 7.1-7.5 | 4 / 2 / 0 |
| FE8 | 3 | Organizer | FR-8.1 to FR-8.4 | 8.1-8.3 | 3 / 1 / 0 |
| FE9 | 3 | Organizer | FR-9.1 to FR-9.4 | 9.1-9.3 | 3 / 1 / 0 |
| FE10 | 4 | Organizer, Judge | FR-10.1 to FR-10.5 | 10.1-10.5 | 4 / 1 / 0 |
| FE11 | 4 | Judge, Organizer | FR-11.1 to FR-11.2 | 11.1-11.2 | 2 / 0 / 0 |
| FE12 | 5 | Organizer | FR-12.1 to FR-12.3 | 12.1-12.3 | 2 / 1 / 0 |
| FE13 | 5 | Organizer, Administrator | FR-13.1 to FR-13.3 | 13.1-13.3 | 2 / 1 / 0 |
| FE14 | Supporting | Organizer | FR-14.1 to FR-14.2 | 14.1-14.2 | 0 / 1 / 1 |
| FE15 | Supporting | Organizer | FR-15.1 to FR-15.3 | 15.1-15.3 | 0 / 2 / 1 |
| FE16 | Supporting | Participant | FR-16.1 to FR-16.3 | 16.1-16.3 | 0 / 2 / 1 |

Expected deliverables of the proposal and the features that deliver them:

| Deliverable | Features |
| --- | --- |
| Web-based management portal for organizers and judges | FE3, FE4, FE8, FE10, FE11, FE12 |
| Web and mobile application for participants | FE5, FE6, FE7, FE16 |
| Administration system for platform management | FE1, FE2 |
| AI module for submission verification and contest analytics | FE9, FE14, FE15 |
| Digital archive of award-winning photographs and historical contest records | FE13 |

## Appendix B. Open Issues

| # | Issue | Proposed handling |
| --- | --- | --- |
| 1 | Blind judging (hiding participant identity from judges) is not mentioned in the proposal | Not included; the team and supervisor decide whether to add it to scope or exclusions |
| 2 | Judge conflict-of-interest handling is not mentioned in the proposal | Same as above |
| 3 | Backend technology and database are not fixed | Decide in Sprint 1 during design |
| 4 | Performance targets in NFR-5 and the thresholds for AI flags are assumptions | Confirm with the supervisor; tune after the AI proof of concept |
| 5 | Tie-breaking rule for equal scores (FR-11.1) | Organizer sets the rule per contest; confirm the default |
| 6 | Mobile app and AI-generated image detection are Should priority | Raise to Must if the supervisor requires them (adds effort, see [02-scope-estimation.md](02-scope-estimation.md)) |
