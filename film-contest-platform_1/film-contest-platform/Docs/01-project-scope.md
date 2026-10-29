# 6. Project Scope & Limitations

## 6.1 Major Features

- **FE1. Account & Access Management:** Registers and authenticates users with JWT, and controls access by role (Administrator, Organizer, Judge, Participant).
- **FE2. System & Master Data Management:** Configures system settings, maintains catalogs of film stocks, ISO, formats, cameras, lenses and labs, and monitors platform activity logs.
- **FE3. Contest Planning & Configuration:** Creates contests with themes, categories, submission and judging schedules, regulations and awards, with reusable templates for recurring contests.
- **FE4. Judging Criteria Setup:** Configures weighted film-specific criteria such as creativity, composition, storytelling, film grain, tonal range, color rendering and scan quality.
- **FE5. Participant Profile & Registration:** Manages personal profiles, contest browsing and registration, and contest history, with organizer approval of registrations.
- **FE6. Film Roll & Frame Management:** Records film rolls and frames (stock, ISO, format, camera, lens, lab, scan specs) and links them to submissions.
- **FE7. Photograph Submission & Tracking:** Uploads scanned photos to secure cloud storage with technical metadata and optional negative/contact-sheet references, and tracks submission status.
- **FE8. Submission Verification:** Checks file format, image quality, deadline and metadata completeness, then lets organizers approve, reject or request revision of flagged items.
- **FE9. AI Image Verification:** Detects duplicate or highly similar photographs and AI-generated images, and flags suspicious submissions for manual review.
- **FE10. Judge Assignment & Judging Workspace:** Assigns judges by category or round, and lets them score, comment, work through multiple rounds and confirm final results.
- **FE11. Score Aggregation & Ranking:** Aggregates judges' scores, ranks submissions and keeps detailed evaluation records for transparency.
- **FE12. Result Publication & Online Exhibition:** Calculates final rankings, publishes official results, and manages awards and an online exhibition of winning works.
- **FE13. Digital Archive:** Stores award-winning photographs with technical metadata, judging comments and contest history, with search and browsing.
- **FE14. AI Keywording & Categorization:** Generates keywords and suggests categories for submitted photographs.
- **FE15. Contest Analytics & Reports:** Produces statistics on participation, submissions, flagged cases and score distribution.
- **FE16. Notifications & Feedback (derived):** Sends results, judge feedback and status updates to participants by email or in-app.

## 6.2 Limitations & Exclusions

- **LI1. No Online Payment:** Entry fees, prize payouts and invoicing are not handled.
- **LI2. No Physical Logistics:** Shipping or receiving negatives and prints, printing, and physical exhibitions are out of scope.
- **LI3. No Social Features:** There is no public voting, likes, follows or public comments; only assigned judges score.
- **LI4. Web-Only Management Portals:** Organizer, judge and admin functions run on the web; only participants have a mobile app.
- **LI5. No Offline Mode:** Submitting and judging require an internet connection.
- **LI6. No External Integration:** There is no integration with film labs, social platforms or other contest systems, and no public API.
- **LI7. AI Supports, Not Replaces, Judges:** AI does not score photographs; artistic and film-specific criteria are judged by humans only.
- **LI8. No Custom AI Training:** Pretrained models and APIs (Computer Vision, OpenAI API) are used.
- **LI9. No Film Code Recognition:** Edge codes, negative strips and contact sheets are stored as optional references, not read automatically.
- **LI10. No Image Editing or Protection:** The platform offers no retouching, watermarking or DRM.
- **LI11. Limited Archive Scope:** Only award-winning works are archived by default.
- **LI12. Film Origin Not Provable:** The system cannot confirm a photo was shot on film; it relies on declared metadata, references and organizer review.
- **LI13. AI Detection Is Probabilistic:** Detection can give false positives and negatives, so results are warnings and organizers decide.
- **LI14. Internal Duplicate Check Only:** Similarity is compared only with images on the platform, not the wider internet.
- **LI15. Metadata Not Cross-Verified:** Declared metadata is checked for completeness and format, not against image data such as EXIF.
- **LI16. Third-Party Dependency:** AI and cloud services affect availability, cost and privacy; if unavailable, verification falls back to manual review.
- **LI17. Capstone-Level Scale and Security:** Performance targets concurrent contests at project scale, and security follows JWT and role-based access without formal certification or penetration testing.
- **LI18. No Legal Adjudication:** Copyright, privacy and model-release disputes are left to the organizers.
- **LI19. Notifications Limited (derived):** Notifications are in-app or email only, with no SMS.
- **LI20. Priority-Based Delivery:** Must features are always delivered; Should and Could features (see [02-scope-estimation.md](02-scope-estimation.md)) are built only if the 8-week schedule allows.
- **LI21. Mobile App Scope:** The Flutter app covers only the participant functions in FE5, FE6 and FE7; all other functions are web-only.
