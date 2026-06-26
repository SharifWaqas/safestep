# 🛡️ SafeStep

> **AI-powered digital safety assistant designed to help older adults recognize scams, understand suspicious digital content, and navigate the online world with confidence.**

> 🚧 **Status:** Active Development

---

## Overview

SafeStep is an AI-powered platform that analyzes screenshots, emails, text messages, and other digital content to identify potential scams and explain suspicious activity in clear, accessible language.

Instead of simply labeling something as "safe" or "unsafe," SafeStep provides understandable explanations, personalized guidance, and educational insights to help users make informed decisions.

The long-term goal is to improve digital safety and digital literacy, especially for older adults who are disproportionately targeted by online scams.

---

## Motivation

Millions of people receive phishing emails, fraudulent text messages, fake websites, and social engineering attacks every day.

Many existing tools focus only on detection.

SafeStep focuses on **understanding**.

The platform explains:

* Why something appears suspicious
* Which scam indicators were detected
* The potential risks involved
* What the user should do next
* How to recognize similar scams in the future

---

## Current Features

* User management
* SQLAlchemy database models
* Analysis workflow architecture
* Risk score domain model
* AI result model
* Upload management
* Session management
* Audit logging
* Modular backend architecture
* FastAPI backend foundation

---

## Planned Features

* Screenshot upload
* OCR pipeline
* AI-powered screenshot analysis
* Email analysis
* SMS analysis
* Website analysis
* Risk scoring engine
* Personalized safety guidance
* Analysis history
* Accessibility-focused interface
* Authentication & authorization
* Docker deployment
* CI/CD pipeline

---

## Architecture

```
                User
                  │
                  ▼
          Upload Screenshot
                  │
                  ▼
              FastAPI API
                  │
                  ▼
          Validation Layer
                  │
                  ▼
            AI Analysis Engine
                  │
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

## Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Pydantic

### Frontend

* Next.js
* TypeScript

### AI

* OpenAI Vision
* OCR Integration (planned)

### DevOps

* Docker
* GitHub Actions (planned)

---

## Project Structure

```
backend/
    app/
        api/
        database/
        models/
        enums/
        services/
        schemas/

frontend/

docs/
```

---

## Engineering Goals

SafeStep is being built using production-oriented software engineering practices:

* Modular architecture
* Domain-driven organization
* Database normalization
* Strong typing
* RESTful APIs
* Secure file handling
* Environment-based configuration
* Audit logging
* Scalable backend design

---

## Roadmap

* [x] Backend project setup
* [x] Database architecture
* [x] Domain models
* [x] Core API foundation
* [ ] Authentication
* [ ] Image upload service
* [ ] OCR integration
* [ ] AI analysis pipeline
* [ ] Risk scoring engine
* [ ] Guidance engine
* [ ] Analysis history
* [ ] Frontend interface
* [ ] Docker deployment
* [ ] Automated testing
* [ ] CI/CD pipeline
* [ ] Public MVP

---

## Why I Built This

I built SafeStep to combine software engineering, backend systems, AI, and accessibility into a single real-world project.

The project emphasizes clean architecture, maintainable code, and practical problem solving while addressing an important social challenge: helping people stay safe online.

---

## License

This project is licensed under the MIT License.
