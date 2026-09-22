# SafeStep

**SafeStep is an AI-powered digital safety companion that helps people understand suspicious digital content, assess the level of risk, and decide what to do next.**

Instead of simply labeling something as a "scam," SafeStep focuses on explaining **what is happening, why it may be suspicious, what action the user should take, and how concerned they should be.**

> **Understand what you're seeing. Know what to do next.**

## Live Application

**Frontend:** https://safestep-rust.vercel.app/

**Backend API:** https://safestep-api-p5fv.onrender.com/

**API Documentation:** https://safestep-api-p5fv.onrender.com/docs

**Health Check:** https://safestep-api-p5fv.onrender.com/health

**Source Code:** https://github.com/SharifWaqas/safestep

---

# The Problem

Suspicious emails, text messages, websites, social media posts, and other digital content are increasingly difficult to evaluate.

For less technical users, particularly older adults, the problem is not always:

> "Is this a scam?"

It is often:

* What does this message actually mean?
* Why is it asking me to do this?
* Is there anything suspicious here?
* How dangerous is this?
* Should I click the link?
* Should I reply?
* What should I do next?
* Should I be worried?

A simple binary classification does not answer those questions.

SafeStep is designed around the idea that **explanation and actionable guidance are just as important as classification.**

---

# The Solution

SafeStep allows a user to upload a screenshot of suspicious digital content.

The system then:

1. Understands the uploaded content using multimodal AI.
2. Extracts relevant evidence from the content.
3. Identifies suspicious characteristics.
4. Determines a risk level.
5. Applies deterministic application-level risk scoring.
6. Generates actionable guidance.
7. Generates calm, contextual reassurance.
8. Stores the analysis for future reference.

### User Flow

```text
Screenshot
    │
    ▼
Upload
    │
    ▼
AI Vision Analysis
    │
    ▼
Structured AI Output
    │
    ▼
Evidence Extraction
    │
    ▼
Risk Classification
    │
    ▼
Deterministic Risk Scoring
    │
    ├───────────────┐
    ▼               ▼
Guidance       Reassurance
    │               │
    └───────┬───────┘
            ▼
       Persist Result
            │
            ▼
       Analysis History
```

---

# Core Features

### Screenshot Analysis

Users can upload screenshots containing suspicious digital content.

Supported formats:

* PNG
* JPG
* JPEG

Maximum upload size:

```text
10 MB
```

Uploaded files are stored in Cloudflare R2 using generated object keys rather than raw user filenames.

### Explainable Analysis

SafeStep does not only return a risk label.

The analysis is designed to explain:

* What the content is saying
* What appears suspicious
* Which evidence contributed to the assessment
* What the user should avoid
* What the user should do next

### Deterministic Risk Scoring

The AI contributes structured evidence and classification, but the application does not blindly trust an LLM-generated risk label.

SafeStep combines AI-generated information with **deterministic application-level risk scoring** to make risk assessment more consistent and explainable.

Risk levels:

```text
SAFE
LOW
MEDIUM
HIGH
VERY_HIGH
```

### Guidance

The system generates practical next steps based on the analysis.

Examples of guidance may include avoiding suspicious links, not providing credentials, independently verifying a request, or contacting an organization through an official channel.

### Reassurance

Suspicious digital content can cause panic.

SafeStep provides contextual reassurance intended to help users understand the situation without unnecessarily increasing anxiety.

### Analysis History

Completed analyses are persisted so users can review previous results.

History includes the analysis status, risk information, AI results, and associated information available to the authenticated user.

### Authentication

SafeStep includes:

* Registration
* Login
* Access JWTs
* Refresh JWTs
* Refresh-token rotation
* Server-side refresh-token hashing
* Session revocation
* Logout
* Ownership checks

---

# System Architecture

SafeStep uses a layered backend architecture designed to keep API concerns, business logic, persistence, and infrastructure responsibilities separated.

```text
                         ┌───────────────────┐
                         │     Next.js       │
                         │     Frontend      │
                         └─────────┬─────────┘
                                   │
                                   │ HTTP
                                   ▼
                         ┌───────────────────┐
                         │      FastAPI      │
                         │    API Layer      │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │     Services      │
                         │   Business Logic  │
                         └─────────┬─────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
          ┌───────────────────┐        ┌───────────────────┐
          │   Repositories    │        │ Infrastructure /  │
          │                   │        │ External Services │
          └─────────┬─────────┘        └─────────┬─────────┘
                    │                            │
                    ▼                            ├── Cloudflare R2
          ┌───────────────────┐                  ├── AI Provider
          │    PostgreSQL     │                  └── Other services
          └───────────────────┘
```

The backend is organized around:

```text
API
 ↓
Services
 ↓
Repositories
 ↓
Database
```

Infrastructure concerns are isolated behind appropriate service/provider abstractions where practical.

---

# Backend Architecture

The backend is built with FastAPI and uses asynchronous SQLAlchemy for database access.

```text
backend/
├── app/
│   ├── ai/
│   │   ├── providers/
│   │   │   ├── nvidia_client.py
│   │   │   └── openai_client.py
│   │   ├── orchestrator.py
│   │   ├── parser.py
│   │   ├── prompts.py
│   │   └── schemas/
│   │
│   ├── api/
│   │   ├── auth.py
│   │   ├── upload.py
│   │   ├── analysis.py
│   │   └── dependencies.py
│   │
│   ├── core/
│   ├── database/
│   ├── enums/
│   ├── middleware/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── config.py
│   └── main.py
│
└── tests/
    ├── ai/
    ├── api/
    ├── core/
    ├── fixtures/
    ├── integration/
    ├── repositories/
    └── services/
```

---

# Analysis Architecture

The analysis endpoint currently executes the analysis pipeline **synchronously from the client's perspective**.

It is not implemented as a background job or distributed worker system.

```text
POST /analyses/{upload_id}
             │
             ▼
      Validate ownership
             │
             ▼
      Create analysis
             │
             ▼
       Run AI pipeline
             │
             ▼
     Parse structured output
             │
             ▼
      Extract evidence
             │
             ▼
   Calculate deterministic risk
             │
             ▼
       Generate guidance
             │
             ▼
      Generate reassurance
             │
             ▼
        Persist results
             │
             ▼
          Audit log
             │
             ▼
         API response
```

Analysis states:

```text
pending
processing
completed
failed
```

Failures are persisted as failed analyses where appropriate, audited, and surfaced through the API.

---

# AI System

SafeStep uses a provider abstraction so the application is not tightly coupled to a single AI provider.

Current provider:

```text
NVIDIA AI
```

Provider support also exists for:

```text
OpenAI
```

The AI subsystem includes:

* Provider abstraction
* Vision/multimodal analysis
* Prompt construction
* Structured output parsing
* AI result persistence
* Evidence extraction
* Risk classification
* Guidance generation
* Reassurance generation

### AI Pipeline

```text
Screenshot
    │
    ▼
Vision / Multimodal Model
    │
    ▼
Structured AI Response
    │
    ▼
Parser
    │
    ▼
Application-Level Validation
    │
    ├── Evidence
    ├── Classification
    └── Analysis information
             │
             ▼
    Deterministic Risk Scoring
             │
       ┌─────┴─────┐
       ▼           ▼
   Guidance    Reassurance
       │           │
       └─────┬─────┘
             ▼
         Persistence
```

The system intentionally does **not** treat the LLM as the sole authority for risk.

---

# Database

SafeStep uses PostgreSQL with SQLAlchemy and Alembic.

Primary entities include:

```text
Users
  │
  ├── Sessions
  │
  ├── Uploads
  │       │
  │       └── Analyses
  │               │
  │               ├── AI Results
  │               └── Risk Scores
  │
  └── Audit Logs
```

### Database Components

* PostgreSQL
* SQLAlchemy AsyncSession
* Alembic migrations
* Repository pattern
* Ownership-aware queries
* Eager loading for required relationships

Current migration head:

```text
46d34abb3b93
```

Migration validation:

```powershell
python -m alembic check
```

Production deployment applies migrations with:

```powershell
python -m alembic upgrade head
```

---

# Authentication & Security

Authentication uses JWT-based access and refresh tokens.

### Access Tokens

Access tokens contain:

```text
sub
type
iat
exp
```

Access token type:

```text
access
```

Refresh token type:

```text
refresh
```

### Refresh Token Security

Refresh tokens are not stored as plaintext in the database.

Instead:

```text
Refresh Token
     │
     ▼
SHA-256
     │
     ▼
Stored Session Hash
```

Refresh-token rotation updates the stored hash.

Session refresh uses database row locking to reduce concurrent refresh races.

A unique database constraint exists on the stored refresh-token hash.

### Other Security Controls

SafeStep also implements:

* Password hashing using `pwdlib`
* JWT validation
* Session revocation
* Token expiration
* Ownership checks
* Upload validation
* Upload size limits
* Controlled CORS
* Environment-based secrets
* Audit logging
* Centralized exception handling
* HTTP status-aware error handling

---

# File Storage

Uploaded screenshots are stored in Cloudflare R2.

The storage key uses a generated UUID rather than the raw user filename.

This avoids using user-controlled filenames as object identifiers.

### Upload Flow

```text
Client
  │
  ▼
FastAPI
  │
  ├── Validate type
  ├── Validate size
  │
  ▼
Cloudflare R2
  │
  ▼
Database Record
```

If database persistence fails after the object is uploaded, the service attempts to remove the R2 object as part of rollback handling.

Uploads associated with an existing analysis cannot be deleted.

This preserves analysis history.

---

# API

Current primary API areas include:

### Authentication

```text
POST /auth/register
POST /auth/login
POST /auth/refresh
POST /auth/logout
```

### Uploads

Upload functionality supports:

```text
PNG
JPG
JPEG
```

with a maximum size of:

```text
10 MB
```

### Analysis

```text
POST /analyses/{upload_id}
GET  /analyses/{analysis_id}
GET  /analyses
```

### Health

```text
GET /health
```

Interactive API documentation is available through FastAPI's Swagger UI in the deployed environment.

---

# Frontend

The frontend is built with:

* Next.js 16.3
* React 19
* TypeScript
* Tailwind CSS 4
* Base UI / shadcn-style components
* lucide-react
* SWR
* sonner
* Vercel Analytics

Routes include:

```text
/
├── /login
├── /register
├── /analyze
├── /analysis/[analysis_id]
├── /history
└── /settings
```

The frontend communicates with the FastAPI backend through the production API.

Authentication state includes:

```text
safestep.access_token
safestep.refresh_token
safestep.user
```

The API client automatically attempts a single token refresh for eligible authenticated requests and coordinates concurrent refresh attempts through a shared refresh promise.

---

# Accessibility

SafeStep is designed around users who may have limited technical experience or accessibility needs.

The frontend includes accessibility work across:

* Login
* Registration
* Analyze
* Upload
* Image preview
* Analysis results
* History
* Settings
* Loading states
* Error states
* Buttons
* Cards

Design priorities include:

* Large, obvious controls
* Strong visual hierarchy
* Clear language
* Reduced cognitive load
* Accessible interaction states
* Minimal technical jargon
* Calm presentation of risk information

---

# Testing

The backend uses:

* pytest
* pytest-asyncio
* anyio

The project has automated tests covering areas including:

* Authentication
* JWT behavior
* Session management
* Token refresh
* Services
* Repositories
* Upload handling
* Analysis behavior
* AI components
* API exception handling
* Ownership and authorization behavior

At established project checkpoints, the backend test suite reached over 119 passing tests, with additional regression coverage subsequently added.

Run the backend tests with:

```powershell
python -m pytest
```

### Important Testing Boundary

The project currently does **not** have a dedicated real-PostgreSQL integration-test infrastructure.

Service and repository tests use mocks and fixtures where appropriate.

Therefore, automated unit/service/repository coverage should not be interpreted as complete production integration-test coverage.

---

# Docker

SafeStep includes a Dockerized local development environment for the backend and PostgreSQL.

The initial Docker architecture is intentionally limited to the backend and PostgreSQL:

```text
Docker Compose
│
├── api
│   └── FastAPI
│
└── postgres
    └── PostgreSQL
         │
         └── Persistent Volume

# Production Deployment

SafeStep currently runs as:

```text
                         GitHub
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
           Vercel                    Render
         Next.js                  FastAPI API
                                      │
                         ┌────────────┼────────────┐
                         ▼            ▼            ▼
                     PostgreSQL      R2        AI Provider
```

### Frontend

The frontend is deployed through Vercel.

Production frontend:

```text
https://safestep-rust.vercel.app/
```

The Vercel project uses:

```text
Root Directory: frontend
Framework: Next.js
```

### Backend

The backend is deployed through Render.

Production backend:

```text
https://safestep-api-p5fv.onrender.com/
```

Health:

```text
https://safestep-api-p5fv.onrender.com/health
```

Swagger:

```text
https://safestep-api-p5fv.onrender.com/docs
```

### Database

Production PostgreSQL is hosted through Render.

### Object Storage

Uploaded screenshots are stored in Cloudflare R2.

### Deployment Verification

The production system has been manually verified end-to-end, including:

* Frontend loading
* Backend health
* Registration
* Login
* Authentication
* CORS
* Upload
* AI analysis
* Analysis results
* History
* Logout
* Re-login

---

# Environment Variables

Secrets and deployment-specific configuration are supplied through environment variables.

Examples include:

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD

JWT_SECRET
JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS

MAX_UPLOAD_SIZE
CORS_ORIGINS

R2_ACCOUNT_ID
R2_ACCESS_KEY_ID
R2_SECRET_ACCESS_KEY
R2_BUCKET_NAME

NVIDIA_API_KEY
NVIDIA_MODEL

OPENAI_API_KEY
OPENAI_MODEL
```

Actual secret values should never be committed to Git.

Use `.env.example` as the reference for required configuration.

---

# Local Development

## Backend

From the **SafeStep root**:

```powershell
python -m venv .venv
```

Activate the environment in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run migrations:

```powershell
python -m alembic upgrade head
```

Start the development server:

```powershell
python -m uvicorn backend.app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

Health:

```text
http://127.0.0.1:8000/health
```

Run tests:

```powershell
python -m pytest
```

## Frontend

From the **frontend directory**:

```powershell
pnpm.cmd install
```

Start development:

```powershell
pnpm.cmd dev
```

Build:

```powershell
pnpm.cmd build
```

Type-check:

```powershell
pnpm.cmd exec tsc --noEmit
```

The frontend uses the configured backend API through:

```text
NEXT_PUBLIC_API_URL
```

and production is configured with:

```text
NEXT_PUBLIC_USE_MOCKS=false
```

---

# Project Structure

```text
SafeStep/
│
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   ├── api/
│   │   ├── core/
│   │   ├── database/
│   │   ├── enums/
│   │   ├── middleware/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── config.py
│   │   └── main.py
│   │
│   └── tests/
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── ...
│
├── alembic/
│
├── requirements.txt
├── pyproject.toml
├── alembic.ini
├── .env.example
├── .gitignore
├── README.md
└── LICENSE
```

Docker-related files will be added at the repository root as the Docker implementation is completed.

---

# Engineering Decisions

SafeStep has deliberately avoided adding infrastructure simply because it is common in modern backend projects.

Some important decisions include:

### Layered Backend

```text
API
 ↓
Service
 ↓
Repository
 ↓
Database
```

This keeps HTTP handling separate from business logic and persistence.

### Deterministic Risk Scoring

The application does not rely entirely on an LLM's final risk label.

AI output provides structured information that is combined with application-level deterministic scoring.

### Refresh Token Hashing

Refresh tokens are stored as hashes rather than plaintext values.

### Refresh Token Rotation

Successful refresh operations rotate the stored refresh-token hash.

### Database Row Locking

Concurrent refresh requests use row-level locking to reduce race conditions.

### Ownership Enforcement

Resources such as uploads and analyses are checked against the authenticated user.

### No Cascade Deletion of Analyzed Uploads

An upload associated with an analysis cannot simply disappear and leave historical analysis records inconsistent.

### Provider Abstraction

AI provider logic is separated from the rest of the application so providers can be changed without rewriting the analysis system.

### Production Simplicity

The current system intentionally does not introduce Redis, distributed workers, queues, Kubernetes, or other infrastructure that the current product does not require.

---

# Current Status

SafeStep currently has:

* Production frontend
* Production backend
* Production PostgreSQL
* Cloudflare R2 storage
* AI-powered screenshot analysis
* Deterministic risk scoring
* Authentication
* Refresh-token rotation
* Session management
* Upload management
* Analysis history
* Audit logging
* Automated backend tests
* Frontend accessibility work
* Production deployment verification

Dockerization is the next infrastructure step.

The initial Docker scope is:

```text
FastAPI + PostgreSQL
```

Production will continue using the existing Vercel + Render architecture unless a separate decision is made to migrate it.

---

# Roadmap

Future engineering work may include:

* Dockerized local development
* Production Docker image
* More comprehensive integration testing
* Background analysis processing
* Improved AI evaluation and testing
* More advanced observability
* Additional AI provider capabilities
* Expanded supported input types
* Further accessibility improvements

These are roadmap items and should not be interpreted as currently implemented functionality.

---

# Why SafeStep?

SafeStep started from a simple observation:

When someone receives a suspicious message, telling them **"this might be a scam"** is often not enough.

People need to understand:

```text
What is happening?
        ↓
Why is it suspicious?
        ↓
How risky is it?
        ↓
What should I do?
        ↓
Should I be worried?
```

SafeStep is an attempt to build that experience as a real software system rather than simply connecting a frontend to an AI API.

The project is intentionally being used to explore practical backend engineering across:

* API design
* Authentication
* Databases
* Transactions
* Storage
* AI orchestration
* Security
* Testing
* Deployment
* System architecture
* Accessibility
* Infrastructure

---

# Technology Stack

| Area                 | Technology                          |
| -------------------- | ----------------------------------- |
| Backend              | Python 3.11                         |
| API                  | FastAPI                             |
| Database             | PostgreSQL                          |
| ORM                  | SQLAlchemy                          |
| Migrations           | Alembic                             |
| Authentication       | JWT / PyJWT                         |
| Password Hashing     | pwdlib                              |
| AI                   | NVIDIA AI / OpenAI provider support |
| Object Storage       | Cloudflare R2                       |
| Frontend             | Next.js                             |
| UI                   | React / Tailwind CSS                |
| Data Fetching        | SWR                                 |
| Testing              | pytest / pytest-asyncio / anyio     |
| Local Infrastructure | Docker Compose                      |
| Frontend Deployment  | Vercel                              |
| Backend Deployment   | Render                              |
| Source Control       | Git / GitHub                        |

---

# License

See [`LICENSE`](LICENSE) for the project's license.
