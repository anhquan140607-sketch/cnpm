# Project Checklist

Tick an item when it is done, then commit and push this file through a pull request.

## Sprint 0. Repository and tools

- [ ] Maintainer creates the private GitHub repository `film-contest-platform` with a README
- [ ] All 5 members and the supervisor are invited and have accepted
- [ ] Branch protection on `main` is enabled (pull request and 1 approval required)
- [ ] Every member installed Git, configured name and email, and cloned the repository
- [ ] Folder structure pushed: `Docs/`, `BE/`, `FE/`, `Skills/`, `README.md`, `Check_list.md`
- [ ] `.gitignore` added (no secrets, no build output)
- [ ] Jira project created with Scrum board, Epics FE1-FE16 and Project-Wide Activities
- [ ] WBS items from `Docs/02-scope-estimation.md` created as Jira issues with estimates and priority labels
- [ ] GitHub for Jira connected to the repository
- [ ] Backend stack (ASP.NET Core or Node.js) and database (PostgreSQL or MySQL) decided

## Documents (Docs/)

- [ ] 01 Project Scope & Limitations reviewed by the team
- [ ] 02 Scope & Estimation reviewed and effort confirmed
- [ ] 03 Management Approach reviewed (roles, Jira workflow)
- [ ] SRS / requirement document
- [ ] Architecture and database design
- [ ] Test plan and test cases
- [ ] Final capstone report

## Sprint 1 (Weeks 1-2): Foundation

- [ ] Architecture, database design and project setup
- [ ] FE1 Account & Access Management (login, RBAC)
- [ ] FE2 System & Master Data Management
- [ ] AI proof of concept (duplicate detection)
- [ ] Sprint review with supervisor, tag `v0.1`

## Sprint 2 (Weeks 3-4): Contest and submission

- [ ] FE3 Contest Planning & Configuration
- [ ] FE4 Judging Criteria Setup
- [ ] FE5 Participant Profile & Registration
- [ ] FE6 Film Roll & Frame Management
- [ ] FE7 Photograph Submission & Tracking
- [ ] Sprint review with supervisor, tag `v0.2`

## Sprint 3 (Weeks 5-6): Verification and judging

- [ ] FE8 Submission Verification
- [ ] FE9 AI Image Verification
- [ ] FE10 Judge Assignment & Judging Workspace
- [ ] FE11 Score Aggregation & Ranking
- [ ] Sprint review with supervisor, tag `v0.3`

## Sprint 4 (Weeks 7-8): Results, extras and delivery

- [ ] FE12 Result Publication & Online Exhibition
- [ ] FE13 Digital Archive
- [ ] Should features if time allows: FE14, FE15, FE16, Flutter screens
- [ ] System testing on staging and load test
- [ ] User Acceptance Testing (Core Flows 1-5 pass)
- [ ] Deployment to Azure or Firebase
- [ ] Final report and demo, tag `v1.0`

## Before every pull request

- [ ] Branch name and commits contain the Jira key
- [ ] No secrets or large files committed
- [ ] At least one reviewer assigned
