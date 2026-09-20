# SafeStep

**AI-powered digital safety companion for understanding suspicious online content.**

SafeStep helps users, especially older adults and less technical users, understand potentially suspicious screenshots and online messages through explainable AI analysis, risk scoring, clear guidance, and reassurance.

### Live Demo

🌐 **Frontend:** https://safestep-rust.vercel.app


## What SafeStep Does

1. Upload a screenshot of a suspicious message, email, or website.
2. SafeStep analyzes the content using a multimodal AI pipeline.
3. Extracts relevant evidence from the content.
4. Determines a risk level.
5. Explains why the content may be suspicious.
6. Provides clear next-step guidance.
7. Provides reassurance without minimizing the potential risk.
8. Stores the analysis in the user's history.


## Engineering Highlights

- Layered FastAPI backend using service and repository patterns
- PostgreSQL with SQLAlchemy and Alembic migrations
- JWT authentication with rotating refresh-token sessions
- Ownership-based authorization for user resources
- Cloudflare R2 object storage for uploaded images
- Multimodal AI analysis pipeline
- Deterministic risk scoring alongside AI-generated analysis
- Audit logging for security-relevant actions
- File validation and upload size/type enforcement
- Transactional failure handling and storage cleanup
- Automated test suite with pytest
- Production deployment with Vercel and Render
- Production PostgreSQL database
- CORS-controlled frontend/backend communication


                         ┌──────────────────────┐
                         │      Next.js         │
                         │      Frontend        │
                         │       Vercel         │
                         └──────────┬───────────┘
                                    │ HTTPS
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │       Backend        │
                         │       Render         │
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
       │ PostgreSQL   │      │ Cloudflare   │      │ AI Provider  │
       │              │      │ R2           │      │              │
       │ Users        │      │ Images       │      │ Vision       │
       │ Sessions     │      │              │      │ Analysis     │
       │ Analyses     │      └──────────────┘      └──────────────┘
       │ Audit Logs   │
       └──────────────┘



## AI Analysis Pipeline

SafeStep separates AI interpretation from deterministic application logic.

```text
Uploaded Image
      ↓
File Validation
      ↓
Object Storage
      ↓
AI Vision Analysis
      ↓
Structured Evidence
      ↓
Risk Classification
      ↓
Deterministic Risk Scoring
      ↓
Guidance Generation
      ↓
Reassurance Generation
      ↓
Persist Analysis




### 6. Add the production section

This is especially important now because **you actually deployed it**.

```md
## Production Deployment

SafeStep is deployed as a production web application.

| Component | Platform |
|---|---|
| Frontend | Vercel |
| Backend | Render |
| Database | Render PostgreSQL |
| Object Storage | Cloudflare R2 |
| Source Control | GitHub |

### Production URLs

- Frontend: https://safestep-rust.vercel.app
- Backend API: https://safestep-api-p5fv.onrender.com
- API Health Check: https://safestep-api-p5fv.onrender.com/health



### 6. Add the production section

This is especially important now because **you actually deployed it**.

```md
## Production Deployment

SafeStep is deployed as a production web application.

| Component | Platform |
|---|---|
| Frontend | Vercel |
| Backend | Render |
| Database | Render PostgreSQL |
| Object Storage | Cloudflare R2 |
| Source Control | GitHub |

### Production URLs

- Frontend: https://safestep-rust.vercel.app
- Backend API: https://safestep-api-p5fv.onrender.com
- API Health Check: https://safestep-api-p5fv.onrender.com/health


## Local Development

### Prerequisites

- Python 3.11+
- Node.js
- pnpm 11+
- PostgreSQL
- Cloudflare R2 account
- AI provider API credentials

### Backend

```bash
git clone https://github.com/SharifWaqas/safestep.git
cd safestep

python -m venv .venv
# activate virtual environment

pip install -r requirements.txt

python -m alembic upgrade head

python -m uvicorn backend.app.main:app --reload


cd frontend
pnpm install
pnpm dev

NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
NEXT_PUBLIC_USE_MOCKS=false



### 8. Add testing

```md
## Testing

Backend tests are run with:

```bash
python -m pytest


### 9. Add a security section

```md
## Security

SafeStep includes:

- JWT access and refresh tokens
- Refresh-token rotation
- Hashed refresh tokens stored server-side
- Row-level ownership checks
- File type and size validation
- Controlled CORS origins
- Audit logging
- Secrets managed through environment variables
- Production database migrations through Alembic

## Why SafeStep?

The goal is not simply to build another AI wrapper.

SafeStep is designed as an example of how AI can be integrated into a real software system with authentication, persistence, storage, security controls, deterministic business logic, accessibility, testing, and production infrastructure.