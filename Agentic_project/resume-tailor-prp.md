# PRP: Resume Tailor and Cover Letter Agent

> Implementation blueprint for parallel agent execution

---

## METADATA

| Field | Value |
|-------|-------|
| **Product** | Resume Tailor and Cover Letter Agent |
| **Type** | SaaS |
| **Version** | 1.0 |
| **Created** | 2026-03-21 |
| **Complexity** | High |

---

## PRODUCT OVERVIEW

**Description:** AI-powered SaaS that helps job seekers tailor resumes and generate personalized cover letters using Anthropic Claude (claude-opus-4-6).

**Value Proposition:** Paste a job description, select your resume, get a tailored resume and cover letter via streaming AI in seconds.

**MVP Scope:**
- [ ] User registration and login (Supabase Auth)
- [ ] Upload and manage resumes (PDF/DOCX via Supabase Storage)
- [ ] Paste job description + AI-tailor resume (streaming)
- [ ] Generate cover letter (streaming)
- [ ] Save and view applications

---

## TECH STACK

| Layer | Technology | Reference |
|-------|------------|-----------|
| Framework | Next.js 14+ App Router + TypeScript | skills/BACKEND.md |
| Database | PostgreSQL via Supabase | skills/DATABASE.md |
| Auth | Supabase Auth | skills/BACKEND.md |
| UI | Tailwind CSS | skills/FRONTEND.md |
| AI | @anthropic-ai/sdk -- claude-opus-4-6 | lib/anthropic/ |
| Storage | Supabase Storage | skills/BACKEND.md |
| Testing | Vitest + Testing Library | skills/TESTING.md |
| Deployment | Docker + GitHub Actions | skills/DEPLOYMENT.md |

---

## DATABASE MODELS

### User (managed by Supabase Auth)
- id: uuid (PK)
- email: string (unique)
- full_name: string
- avatar_url: string (nullable)
- created_at: timestamp

### Resume
- id: uuid (PK)
- user_id: uuid (FK -> auth.users, CASCADE DELETE)
- title: string
- file_url: string (Supabase Storage path)
- file_type: enum (pdf, docx)
- skills: text[]
- experience: text
- is_default: boolean (default false)
- version: integer (default 1)
- uploaded_at: timestamp
- updated_at: timestamp

### Application
- id: uuid (PK)
- user_id: uuid (FK -> auth.users, CASCADE DELETE)
- resume_id: uuid (FK -> resumes, SET NULL on delete)
- job_title: string
- company: string
- job_description: text
- tailored_resume: text (nullable -- populated by Claude)
- cover_letter: text (nullable -- populated by Claude)
- status: enum (draft, saved, applied, interviewing, rejected, offered)
- applied_at: timestamp (nullable)
- created_at: timestamp
- updated_at: timestamp

### RLS Policies (all tables)
- SELECT/INSERT/UPDATE/DELETE: only where auth.uid() = user_id
- Enforced via Supabase Row Level Security

### DB Trigger
- On resumes INSERT/UPDATE: if is_default = true, set all other user resumes to is_default = false

---

## MODULES

### Module 1: Authentication
**Agents:** DATABASE-AGENT + BACKEND-AGENT + FRONTEND-AGENT

**API Routes:**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/signup | Create account via Supabase Auth |
| POST | /api/auth/login | Login, return session |
| POST | /api/auth/logout | Invalidate session |
| GET | /api/auth/me | Get current user profile |

**Middleware:** middleware.ts -- protects /dashboard/*, /resumes/*, /applications/*

**Pages:**
| Route | Page | Key Components |
|-------|------|----------------|
| /login | LoginPage | EmailInput, PasswordInput, SubmitButton |
| /register | RegisterPage | RegisterForm |
| /forgot-password | ForgotPasswordPage | EmailInput, BackToLoginLink |
| /profile | ProfilePage (protected) | ProfileForm, AvatarUpload |

---

### Module 2: Resume Manager
**Agents:** DATABASE-AGENT + BACKEND-AGENT + FRONTEND-AGENT

**API Routes:**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/resumes | List all user resumes |
| POST | /api/resumes | Create resume record |
| GET | /api/resumes/{id} | Get resume detail |
| PUT | /api/resumes/{id} | Update title/tags |
| DELETE | /api/resumes/{id} | Delete resume + Supabase Storage file |
| PUT | /api/resumes/{id}/default | Set as default (DB trigger clears others) |
| GET | /api/resumes/{id}/download | Generate signed download URL |
| POST | /api/uploads/resume | Upload PDF/DOCX to Supabase Storage |

**Validation:** Zod schema -- file type (pdf/docx only), size (max 5MB)
**Storage path format:** resumes/{user_id}/{uuid}-{original_filename}

**Pages:**
| Route | Page | Key Components |
|-------|------|----------------|
| /resumes | ResumeListPage | ResumeCard, ResumeUploadModal, EmptyState, Skeleton |
| /resumes/{id} | ResumeDetailPage | ResumePreview, DownloadBtn, SetDefaultBtn, DeleteBtn |
| (modal) | ResumeUploadModal | DragDropZone, FileTypeHint, ProgressBar |

---

### Module 3: Job Applications (Core AI Feature)
**Agents:** DATABASE-AGENT + BACKEND-AGENT + FRONTEND-AGENT

**API Routes:**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/applications | List all user applications |
| POST | /api/applications | Create new application |
| GET | /api/applications/{id} | Get application detail |
| PUT | /api/applications/{id} | Update application |
| DELETE | /api/applications/{id} | Delete application |
| POST | /api/applications/{id}/tailor | Stream AI-tailored resume via Claude |
| POST | /api/applications/{id}/cover-letter | Stream AI-generated cover letter |
| GET | /api/applications/{id}/export | Export tailored resume + cover letter |

**AI Implementation Pattern:**
  // lib/anthropic/client.ts
  import Anthropic from "@anthropic-ai/sdk";
  export const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

  // In API route handler:
  const stream = anthropic.messages.stream({
    model: "claude-opus-4-6",
    max_tokens: 64000,
    thinking: { type: "adaptive" },
    messages: [{ role: "user", content: RESUME_TAILOR_PROMPT(jobDesc, resume) }],
  });
  return new Response(stream.toReadableStream(), {
    headers: { "Content-Type": "text/event-stream" },
  });

**Rate Limiting:** Max 10 AI requests per user per hour (enforced server-side)
**Prompts:** See lib/anthropic/prompts.ts -- RESUME_TAILOR_PROMPT, COVER_LETTER_PROMPT

**Pages:**
| Route | Page | Key Components |
|-------|------|----------------|
| /applications | ApplicationListPage | ApplicationCard, StatusBadge, FilterBar, EmptyState |
| /applications/new | NewApplicationPage | JobDescriptionForm, ResumeSelector, SubmitBtn |
| /applications/{id} | ApplicationDetailPage | TailoredResumeView, CoverLetterView, StreamingIndicator, ExportBtn |

**useAIStream hook:** Reads SSE events and updates state incrementally for live streaming UX

---

### Module 4: Dashboard
**Agents:** BACKEND-AGENT + FRONTEND-AGENT

**API Routes:**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/dashboard/stats | Aggregate stats from applications + resumes |

**Stats Response Shape:**
  { totalApplications: number, resumesUploaded: number,
    byStatus: { draft, saved, applied, interviewing, rejected, offered },
    recentActivity: Application[] (last 5) }

**Pages:**
| Route | Page | Key Components |
|-------|------|----------------|
| /dashboard | DashboardPage | StatCard x4, StatusChart, ActivityFeed, QuickStartBtn |

---

## PHASE EXECUTION PLAN

**Phase 1: Foundation (4 agents in parallel)**
- DATABASE-AGENT: Supabase schema, RLS policies, storage buckets, DB functions
- BACKEND-AGENT: Next.js project setup, app router structure, API route scaffolding, middleware
- FRONTEND-AGENT: Tailwind config, shared components (Button, Input, Card, Modal), layout
- DEVOPS-AGENT: Environment files, Vercel config, Supabase project setup docs

**Validation Gate 1:**
```bash
npm install
npm run build
npx supabase db push (or manual SQL execution)
```

**Phase 2: Modules (parallel per module)**
- Auth Module: Supabase Auth integration + Login/Register/Callback pages
- Resume Module: Upload API + Storage + Resume list/detail pages
- Job Applications Module: AI tailoring API (streaming) + Application form/list pages
- Dashboard Module: Stats API + Dashboard page with charts

**Validation Gate 2:**
```bash
npm run lint
npm run type-check
```

**Phase 3: Quality (3 agents in parallel)**
- TEST-AGENT: Jest + React Testing Library, API route tests, 80%+ coverage
- REVIEW-AGENT: Security audit (RLS policies, input validation, rate limiting), performance
- RESEARCH-AGENT: Anthropic SDK best practices, Next.js 14 App Router patterns

**Final Validation:**
```bash
npm run build
npm start
curl localhost:3000/api/health
```

---

## VALIDATION GATES

| Gate | Commands |
|------|----------|
| 1 | `npm install`, `npm run build`, Supabase schema applied |
| 2 | `npm run lint`, `npm run type-check` |
| 3 | `npm test -- --coverage`, coverage >= 80% |
| Final | `npm run build && npm start`, health check passes |

---

## ENVIRONMENT VARIABLES

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Anthropic
ANTHROPIC_API_KEY=sk-ant-your-key

# App
NEXT_PUBLIC_APP_URL=http://localhost:3000
NODE_ENV=development
```

---

## ACCEPTANCE CRITERIA

### Authentication
- [ ] User can sign up with email/password via Supabase Auth
- [ ] User can log in with Google OAuth via Supabase Auth
- [ ] Protected routes redirect unauthenticated users to /login
- [ ] Supabase Auth session persists across page refreshes
- [ ] User can log out and session is cleared

### Resume Manager
- [ ] User can upload PDF/DOCX files (max 10MB) to Supabase Storage
- [ ] Uploaded resumes appear in the resume list with title and date
- [ ] User can set a resume as default
- [ ] User can delete a resume (removes from Storage + database)
- [ ] Resume content is extracted and stored for AI processing
- [ ] RLS ensures users can only see their own resumes

### Job Applications (AI Core)
- [ ] User can paste a job description and select a base resume
- [ ] AI tailors resume content to the job description (streaming response)
- [ ] AI generates a cover letter (streaming response)
- [ ] Tailored resume and cover letter are saved to the database
- [ ] Application status can be updated (saved, applied, interviewing, rejected, offered)
- [ ] Rate limiting: max 10 AI requests per user per hour
- [ ] RLS ensures users can only see their own applications

### Dashboard
- [ ] Dashboard shows total applications, resumes uploaded, applications by status
- [ ] Recent activity feed shows last 5 applications
- [ ] Stats update in real-time after new applications are created
- [ ] Quick-start button navigates to new application form

### File Uploads
- [ ] Only PDF and DOCX files are accepted
- [ ] Files larger than 10MB are rejected with clear error message
- [ ] Upload progress is shown to the user
- [ ] Supabase Storage RLS prevents accessing other users' files

### Quality
- [ ] All TypeScript strict mode checks pass (no errors)
- [ ] ESLint passes with no warnings
- [ ] Test coverage >= 80% for API routes and utility functions
- [ ] No hardcoded API keys or secrets in code
- [ ] All API inputs validated with Zod schemas

---

## NEXT STEP

Execute with parallel agents:
```
/execute-prp PRPs/resume-tailor-prp.md
```

