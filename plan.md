# Universal Media Converter — Development Plan

> Derived from `universal_media_converter_sdd.md` (Spec-Driven Development Document v2.0)

---

## Overview

This plan breaks the **Universal Media Converter** into **8 discrete phases**. Each phase produces a working, testable increment that can be committed and pushed to GitHub independently.

**Architecture:**

- **Frontend:** Next.js 14 (App Router), Tailwind CSS, ShadCN UI, Framer Motion
- **Backend:** Node.js + Express
- **Queue:** Redis + BullMQ (worker queue)
- **Workers:** Separate worker services for CPU-heavy conversions
- **Engines:** FFmpeg (video), Sharp (images), Pandoc/LibreOffice (documents)

**Repository:** `Universal-Media-Converter`
**Branching:** `main` — each phase is committed directly to `main` (or via PR if preferred)

---

## Phase 1: Project Setup & Infrastructure

**Goal:** Initialize monorepo structure, install dependencies, and configure dev tooling.

**Tasks:**

1. Create root folder structure:
   ```
   universal-media-converter/
   ├── frontend/
   ├── backend/
   ├── workers/
   ├── uploads/
   ├── outputs/
   ├── temp/
   ├── docs/
   ├── .gitignore
   └── README.md
   ```
2. Initialize `frontend/` as Next.js project with TypeScript, Tailwind, ShadCN
3. Initialize `backend/` as Node.js/Express project with TypeScript
4. Initialize `workers/` as Node.js project with TypeScript
5. Add root-level convenience scripts (`package.json` or scripts)
6. Add `.gitignore`, `README.md`, and basic documentation
7. Add Docker Compose file for Redis (queue dependency)

**Deliverables:**

- Runnable dev environments for frontend (`npm run dev`) and backend (`npm run dev`)
- Redis service available via Docker
- Clean GitHub repo structure

**Git Checkpoint:** `chore: initialize project infrastructure`

---

## Phase 2: Backend API Foundation

**Goal:** Build the core Express API, file upload infrastructure, and job queue system.

**Tasks:**

1. Set up Express server with middleware (CORS, Helmet, rate limiting)
2. Configure Multer for file uploads with:
   - File type validation (whitelist extensions)
   - File size limits
   - Filename sanitization
   - Storage to `uploads/` directory
3. Set up Redis connection and BullMQ queue (`conversionQueue`)
4. Implement API endpoints:
   - `POST /upload` — accept files, return file metadata + temp ID
   - `POST /convert` — accept `fileId` + `outputFormat` + `options`, enqueue job, return `jobId`
   - `GET /status/:jobId` — return job status (`pending`, `processing`, `completed`, `failed`) + progress
   - `GET /download/:jobId` — stream converted file from `outputs/`
5. Implement temp file cleanup (delete from `uploads/` and `outputs/` after 24h)
6. Add centralized error handling

**Deliverables:**

- API tested via Postman/curl
- Jobs can be enqueued and their status retrieved
- Files are uploaded and sanitized correctly

**Git Checkpoint:** `feat: backend api foundation with upload and job queue`

---

## Phase 3: Frontend Foundation

**Goal:** Build the Next.js shell, shared UI components, and global state/layout.

**Tasks:**

1. Configure Tailwind theme (colors, shadows, rounded corners matching SaaS aesthetic)
2. Set up global layout with navigation and footer
3. Create shared components:
   - `ConverterCard` (icon, title, description, CTA)
   - `UploadZone` (drag-and-drop + file picker)
   - `ToastNotification` (ShadCN Sonner)
4. Build the **Dashboard/Home page** with:
   - Video Converter Card
   - Image Converter Card
   - Document Converter Card
5. Set up API client utilities (fetch wrappers for backend)
6. Implement responsive design (mobile-first)

**Deliverables:**

- Visually polished dashboard
- Clicking a converter card navigates to its route (`/convert/video`, etc.)
- Upload zone is interactive (UI only, not yet wired to backend)

**Git Checkpoint:** `feat: frontend foundation with dashboard and shared components`

---

## Phase 4: Image Converter Module (End-to-End)

**Goal:** Complete vertical slice — Image conversion works from UI to worker.

**Tasks:**

1. **Frontend:**
   - Build `/convert/image` page
   - Add `FormatSelector` component (JPG, PNG, WEBP, BMP, TIFF)
   - Add `AdvancedOptions` (resize width/height, quality/compression)
   - Wire upload → backend → poll status → show `ProgressTracker`
   - Show `DownloadCard` on completion
2. **Backend:**
   - Update `/convert` endpoint to validate image-specific options
3. **Worker:**
   - Create image worker using **Sharp**
   - Support input: JPG, PNG, WEBP, BMP, TIFF, GIF
   - Support output: JPG, PNG, WEBP, BMP, TIFF
   - Implement resize, quality/compression, transparency preservation
   - Update job progress in BullMQ
4. **Integration:**
   - Test full flow: upload PNG → convert to WEBP with resize → download

**Deliverables:**

- Users can convert images via the UI
- Batch image conversion works (multiple files queued)
- Progress is visible in real-time

**Git Checkpoint:** `feat: image converter module (end-to-end)`

---

## Phase 5: Document Converter Module (End-to-End)

**Goal:** Complete vertical slice — Document conversion works from UI to worker.

**Tasks:**

1. **Frontend:**
   - Build `/convert/document` page
   - Format selector: PDF, DOCX, TXT, HTML
   - Minimal advanced options (preserve formatting toggle)
   - Reuse UploadZone, ProgressTracker, DownloadCard
2. **Backend:**
   - Validate document-specific conversions
3. **Worker:**
   - Create document worker using **Pandoc** (primary) and **LibreOffice** (fallback for complex DOCX)
   - Support input: PDF, DOCX, TXT, HTML, MD
   - Support output: PDF, DOCX, TXT, HTML
   - Handle formatting preservation best-effort
4. **Integration:**
   - Test: MD → PDF, DOCX → TXT, HTML → PDF

**Deliverables:**

- Document conversions are functional
- Common edge cases handled (unsupported combos, formatting loss warnings)

**Git Checkpoint:** `feat: document converter module (end-to-end)`

---

## Phase 6: Video Converter Module (End-to-End)

**Goal:** Complete vertical slice — Video conversion works from UI to worker.

**Tasks:**

1. **Frontend:**
   - Build `/convert/video` page
   - Format selector: MP4, AVI, MOV, MKV, WEBM
   - Advanced options: resolution (dropdown), bitrate, compression level
   - Reuse shared components
2. **Backend:**
   - Validate video-specific options
   - Handle large file uploads (consider chunked upload if needed)
3. **Worker:**
   - Create video worker using **FFmpeg**
   - Support input: MP4, AVI, MOV, MKV, WMV, FLV, WEBM
   - Support output: MP4, AVI, MOV, MKV, WEBM
   - Implement resolution scaling, bitrate adjustment, compression
   - Extract audio (future-ready stub if time permits)
   - Report progress (parse FFmpeg stderr for percentage)
4. **Integration:**
   - Test: AVI → MP4, MKV → WEBM with resolution change

**Deliverables:**

- Video conversions are functional
- Progress reporting is accurate for long-running jobs

**Git Checkpoint:** `feat: video converter module (end-to-end)`

---

## Phase 7: Batch Processing, Progress & Polish

**Goal:** Ensure batch workflows are robust, UI is polished, and performance targets are met.

**Tasks:**

1. **Batch Processing:**
   - UploadZone supports multi-file drop
   - Backend accepts arrays of files in `/upload`
   - `/convert` accepts batch job configuration
   - Workers process jobs concurrently (configurable concurrency)
   - UI shows per-file status in a list/table view
2. **Progress Tracking:**
   - ProgressTracker shows: progress bar, status label, estimated time
   - Global conversion history (in-memory or localStorage for MVP)
3. **UI/UX Polish:**
   - Framer Motion animations (page transitions, card hovers, progress bars)
   - Loading skeletons
   - Error states with retry buttons
   - Empty states
4. **Security & Performance:**
   - Strict file type validation (magic numbers + extension)
   - Size limits enforced
   - Rate limiting on API
   - Temp file cleanup scheduled (node-cron or BullMQ delayed jobs)

**Deliverables:**

- Batch conversion is smooth and reliable
- UI feels modern and responsive
- No orphaned temp files

**Git Checkpoint:** `feat: batch processing, progress tracking, and ui polish`

---

## Phase 8: Testing, Documentation & Final QA

**Goal:** Ensure the application is stable, documented, and ready for use.

**Tasks:**

1. **Testing:**
   - Unit tests for utility functions (backend + workers)
   - API integration tests (Supertest)
   - Frontend component tests (basic smoke tests)
2. **Documentation:**
   - Update `README.md` with setup instructions, env vars, and architecture
   - Add API documentation (OpenAPI/Swagger or markdown)
   - Add `CONTRIBUTING.md` and `CHANGELOG.md`
3. **Final QA against Acceptance Criteria:**
   - ✅ Users can upload supported files
   - ✅ Users can select output formats
   - ✅ Files convert successfully
   - ✅ Progress is visible
   - ✅ Results are downloadable
   - ✅ Batch conversion works
   - ✅ Errors are handled gracefully
4. **Deployment Prep:**
   - Add production build scripts
   - Add environment configuration templates (`.env.example`)

**Deliverables:**

- Test suite passes
- Documentation is complete
- All acceptance criteria satisfied

**Git Checkpoint:** `docs: final testing, documentation, and qa`

---

## Git Workflow

**Commit Strategy:**

- Each phase is a **single commit** with a clear conventional commit message
- If a phase is very large, split into logical sub-commits within the phase, then push once the phase is complete

**Push Cadence:**

- At the end of **every phase**, run:
  ```bash
  git add .
  git commit -m "<phase message>"
  git push origin main
  ```

**Branching (Optional):**

- Create feature branches per phase if you prefer PR-based workflow:
  ```bash
  git checkout -b phase/<n>-<name>
  # ... work ...
  git push -u origin phase/<n>-<name>
  # merge via PR or git merge
  ```

---

## Tech Stack Summary

| Layer           | Technology                                                     |
| --------------- | -------------------------------------------------------------- |
| Frontend        | Next.js 14, TypeScript, Tailwind CSS, ShadCN UI, Framer Motion |
| Backend         | Node.js, Express, TypeScript, Multer, BullMQ                   |
| Queue           | Redis                                                          |
| Workers         | Node.js, TypeScript, BullMQ workers                            |
| Video Engine    | FFmpeg                                                         |
| Image Engine    | Sharp                                                          |
| Document Engine | Pandoc, LibreOffice                                            |
| DevOps          | Docker Compose (Redis), PM2 (optional)                         |

---

## Risk Mitigation

| Risk                                                | Mitigation                                                              |
| --------------------------------------------------- | ----------------------------------------------------------------------- |
| FFmpeg/Sharp/Pandoc not installed on target machine | Provide Docker setup for workers; document install steps                |
| Large video uploads timeout                         | Implement chunked upload or increase limits; add progress during upload |
| Redis unavailable                                   | Add graceful degradation (in-memory queue for local dev)                |
| Format support gaps                                 | Validate formats early in upload; show unsupported warnings in UI       |
| Worker crashes mid-conversion                       | BullMQ retry logic with exponential backoff                             |

---

## Estimates (Relative)

| Phase                        | Relative Effort |
| ---------------------------- | --------------- |
| Phase 1: Setup               | Small           |
| Phase 2: Backend API         | Medium          |
| Phase 3: Frontend Foundation | Medium          |
| Phase 4: Image Converter     | Medium          |
| Phase 5: Document Converter  | Medium          |
| Phase 6: Video Converter     | Large           |
| Phase 7: Batch & Polish      | Medium          |
| Phase 8: Testing & Docs      | Small           |

**Total:** 8 phases, each pushed to GitHub upon completion.

---

## Next Step

Ready to begin **Phase 1: Project Setup & Infrastructure**.
