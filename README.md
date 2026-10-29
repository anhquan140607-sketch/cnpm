# AI-powered Film Photography Contest Management Platform

Vietnamese: Nền tảng tổ chức và quản lý cuộc thi nhiếp ảnh phim tích hợp trí tuệ nhân tạo

A web and mobile platform that manages film photography contests from planning and registration to submission verification, judging, result publication and digital archiving. Every submission carries film metadata (film stock, camera, lens, ISO, format, frame number, lab, scanning specs), and AI helps organizers detect duplicate and AI-generated images, categorize photos and produce analytics.

## Team and timeline

- Team: 5 members
- Duration: 8 weeks, Agile Scrum, 4 sprints of 2 weeks
- Management: Jira (backlog, sprints) and GitHub (source code and documents)

## System roles

| Role | Main responsibilities |
| --- | --- |
| Administrator | Users and permissions, system settings, master data, activity monitoring |
| Contest Organizer | Contests, categories, judging criteria, registrations, verification, judge assignment, results, awards |
| Judge | Review assigned submissions, score and comment, multiple rounds, confirm final results |
| Participant | Profile, contest registration, film roll and frame records, submissions, tracking, results |

## Technology stack

| Layer | Technology |
| --- | --- |
| Web | ReactJS / Next.js |
| Mobile | Flutter (participant app) |
| Backend | ASP.NET Core Web API or Node.js (Express), to be chosen in the design phase |
| Database | PostgreSQL or MySQL, to be chosen in the design phase |
| AI | Computer Vision, OpenAI API, image similarity detection |
| Storage | Firebase Storage or Azure Blob Storage |
| Deployment | Microsoft Azure / Firebase |
| Version control | GitHub |

## Repository structure

```
film-contest-platform/
├── Docs/            Project documents (.md), pushed by members through Git
├── BE/              Backend source code
├── FE/              Frontend source code (web, mobile)
├── Skills/          Reusable skill and prompt files for the team
├── README.md        This file
└── Check_list.md    Team checklist
```

| Document | Content |
| --- | --- |
| [Docs/01-project-scope.md](Docs/01-project-scope.md) | Major features (FE1-FE16) and limitations and exclusions (LI1-LI21) |
| [Docs/02-scope-estimation.md](Docs/02-scope-estimation.md) | WBS, complexity, priority and effort in man-hours |
| [Docs/03-management-approach.md](Docs/03-management-approach.md) | Objectives, risks, Scrum process, Jira setup, quality management |
| [Docs/04-git-workflow-guide.md](Docs/04-git-workflow-guide.md) | Step-by-step GitHub guide for the team (Vietnamese) |

## Getting started

```bash
git clone https://github.com/<owner>/film-contest-platform.git
cd film-contest-platform
git checkout -b <JIRA-KEY>-short-description
```

Read [Docs/04-git-workflow-guide.md](Docs/04-git-workflow-guide.md) before your first commit.

## Contributing rules

- Never push directly to `main`. Work on a branch named after the Jira issue key and open a pull request.
- Every commit message starts with the Jira key, for example `FILM-12: add film roll form`.
- At least one teammate reviews each pull request (two for authentication and scoring).
- Tick items in [Check_list.md](Check_list.md) when you finish them.
