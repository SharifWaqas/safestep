# 🛡️ SafeStep

> **AI-powered digital safety assistant that helps people identify scams, understand suspicious digital content, and make safer online decisions.**

🚧 **Project Status:** Active Development

---

## Overview

SafeStep is an AI-powered platform designed to help users—especially older adults—recognize scams and understand suspicious digital content.

Rather than simply classifying content as **safe** or **unsafe**, SafeStep explains:

* Why something appears suspicious
* Which scam indicators were detected
* The potential level of risk
* Recommended next steps
* Educational guidance to help users recognize similar scams in the future

The goal is to improve digital safety and digital literacy through clear, accessible AI-powered explanations.

---

## Why SafeStep?

Online scams are becoming increasingly sophisticated, targeting millions of people every year. While many existing tools focus solely on detection, they often fail to explain **why** something is dangerous.

SafeStep was created to bridge that gap by combining AI analysis with human-friendly explanations, helping users build confidence when navigating emails, text messages, websites, and other digital content.

---

## Current Progress

The project is currently under active development.

### ✅ Implemented

* FastAPI backend foundation
* SQLAlchemy ORM integration
* PostgreSQL database architecture
* Modular backend structure
* User domain model
* Upload domain model
* Analysis domain model
* AI Result domain model
* Risk Score domain model
* Session management model
* Audit Log model
* Enum architecture
* Database initialization

### 🚧 In Progress

* Authentication & Authorization
* Service layer implementation
* API endpoints
* Business logic
* Database migrations

### 📌 Planned

* Screenshot analysis
* OCR pipeline
* AI-powered scam detection
* Email analysis
* SMS analysis
* Website analysis
* Personalized guidance engine
* Analysis history
* Accessibility-focused UI
* Docker deployment
* Automated testing
* CI/CD pipeline

---

## System Architecture

```text
                  User
                    │
                    ▼
          Upload Screenshot / Email / Text
                    │
                    ▼
               FastAPI Backend
                    │
                    ▼
            Validation & Processing
                    │
                    ▼
              AI Analysis Engine
          ┌─────────┼─────────┐
          ▼         ▼         ▼
        OCR     Scam Analysis  Risk Scoring
          │         │         │
          └─────────┼─────────┘
                    ▼
          Guidance Generation
                    │
                    ▼
              PostgreSQL Database
                    │
                    ▼
             Analysis History
```

---

## Technology Stack

| Layer          | Technologies                    |
| -------------- | ------------------------------- |
| **Backend**    | Python, FastAPI                 |
| **Database**   | PostgreSQL                      |
| **ORM**        | SQLAlchemy                      |
| **Validation** | Pydantic                        |
| **Frontend**   | Next.js, TypeScript *(planned)* |
| **AI**         | OpenAI Vision *(planned)*       |
| **OCR**        | Planned                         |
| **Deployment** | Docker *(planned)*              |
| **CI/CD**      | GitHub Actions *(planned)*      |

---

## Engineering Highlights

SafeStep is being built using modern software engineering principles:

* Modular Monolith Architecture
* Domain-Driven Organization
* SQLAlchemy ORM
* RESTful API Design
* Environment-based Configuration
* Secure File Upload Design
* Audit Logging
* Risk Scoring Pipeline
* AI Integration
* Accessibility-First Design
* Scalable Project Structure

---

## Project Structure

```text
SafeStep/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── database/
│   │   ├── enums/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── utils/
│   │
│   └── tests/
│
├── frontend/
│
├── docs/
│
├── .gitignore
├── README.md
└── LICENSE
```

---

## Getting Started

### Clone the repository

```bash
git clone https://github.com/SharifWaqas/safestep.git
cd safestep
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the virtual environment

**Windows**

```bash
.venv\Scripts\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file in the project root and add the required configuration values.

### Start the application

```bash
uvicorn backend.app.main:app --reload
```

> **Note:** The startup command may change as the project structure evolves.

---

## Roadmap

* [x] Repository setup
* [x] Backend architecture
* [x] Database design
* [x] SQLAlchemy models
* [x] Domain modeling
* [ ] Authentication
* [ ] Upload service
* [ ] OCR integration
* [ ] AI analysis engine
* [ ] Risk scoring engine
* [ ] Guidance generation
* [ ] Analysis history
* [ ] Frontend application
* [ ] Docker support
* [ ] Automated testing
* [ ] GitHub Actions CI/CD
* [ ] Public MVP Release

---

## Project Goals

SafeStep is intended to demonstrate:

* Backend software engineering
* API design
* Database modeling
* AI integration
* Secure application architecture
* Accessibility-focused software design
* Production-ready development practices

---

## Contributing

Contributions, suggestions, and feedback are welcome.

As the project continues to evolve, issues and feature requests will be used to track development.

---

## License

This project is licensed under the MIT License.

---

## Disclaimer

SafeStep is an educational and research project currently under active development. AI-generated analyses are intended to assist users and should not be considered professional legal, cybersecurity, or financial advice.
