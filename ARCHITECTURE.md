# DealSense AI — Architecture

## Overview

DealSense AI is an AI-powered due diligence platform designed for Private Equity firms, Venture Capital firms, M&A advisors, investment banks, and acquisition professionals.

The system follows a modular architecture where each module has a single primary responsibility. The objective is to keep the codebase maintainable, extensible, and production-ready.

---

# High-Level Flow

```
User
    │
    ▼
Streamlit UI (Temporary)
    │
    ▼
pipeline.py
    │
    ▼
analysis.py
    │
    ├───────────────► scraper.py
    │
    ├───────────────► research.py
    │
    ├───────────────► tavily_search.py
    │
    ▼
OpenRouter
(Gemini Model)
    │
    ▼
JSON Response
    │
    ▼
Pydantic Models
    │
    ▼
Scoring Engine
    │
    ▼
Recommendation Engine
    │
    ▼
Cache
    │
    ▼
Streamlit UI
```

---

# Module Responsibilities

## app.py

Purpose

The temporary Streamlit interface.

Responsibilities

* Accept company URL
* Trigger pipeline
* Display analysis
* Display scores
* Display recommendations

Should NOT

* Contain business logic
* Call LLMs directly
* Parse JSON
* Perform research

---

## pipeline.py

Purpose

Single entry point into the backend.

Responsibilities

* Start the due diligence workflow
* Coordinate backend execution
* Provide a stable entry point for the frontend

Current Responsibilities

* Invoke analysis
* Pass refresh options

Future Responsibilities

* Workflow orchestration
* Logging
* Metrics
* Parallel execution
* Background jobs

---

## analysis.py

Purpose

Core AI analysis engine.

Responsibilities

* Collect research from internal modules
* Build the LLM prompt
* Call OpenRouter
* Parse JSON response
* Validate with Pydantic
* Calculate acquisition score
* Generate recommendation
* Save and load cache

Should NOT

* Render UI
* Store application state
* Handle frontend logic

---

## scraper.py

Purpose

Website scraping.

Responsibilities

* Download website content
* Extract readable HTML/text

Should NOT

* Analyze companies
* Score businesses

---

## research.py

Purpose

Research preprocessing.

Responsibilities

* Convert website content into cleaner context
* Improve information quality before sending to the LLM

---

## tavily_search.py

Purpose

External web intelligence.

Responsibilities

* Search for company information beyond the website
* Improve analysis with external context

---

## llm.py

Purpose

LLM configuration.

Responsibilities

* Configure OpenRouter
* Store client initialization
* Centralize model access

Should NOT

* Contain prompts
* Contain analysis logic

---

## prompts.py

Purpose

Prompt management.

Responsibilities

* Store system prompts
* Store prompt templates
* Keep prompting separate from business logic

---

## models.py

Purpose

Structured data models.

Responsibilities

* Pydantic validation
* Data structures
* Type safety

Primary Models

* CompanyAnalysis
* Product
* SWOT
* Competitor
* Signals

---

## scoring.py

Purpose

Investment scoring engine.

Responsibilities

* Evaluate investment quality
* Calculate acquisition score
* Apply scoring rules

Should NOT

* Call AI
* Parse JSON

---

## recommendation.py

Purpose

Recommendation engine.

Responsibilities

Convert acquisition score into an investment recommendation.

Example

* Strong Buy
* Buy
* Watch
* Avoid

---

## cache.py

Purpose

Local caching.

Responsibilities

* Save completed analyses
* Load previous analyses
* Reduce repeated API calls

---

## constants.py

Purpose

Shared configuration.

Responsibilities

* Default model
* Shared constants
* Configuration values

---

# Current Technology Stack

Backend

* Python
* Streamlit
* Pydantic
* OpenRouter
* Gemini
* Jina AI
* Tavily Search

Future Frontend

* React
* Next.js
* Tailwind CSS
* Framer Motion

Future Backend

* FastAPI
* PostgreSQL
* Redis
* Docker

---

# Design Principles

The architecture follows these principles:

* Single Responsibility Principle
* Modular design
* Production-ready code
* Minimal duplication
* Reusable components
* Clear separation of concerns
* Extensible architecture

---

# Current Development Phase

The backend foundation is complete.

Current focus:

* AI analysis quality
* Research quality
* Evidence engine
* Investment intelligence

The frontend redesign will begin after the backend reaches a stable production-ready state.

---

# Long-Term Vision

The Streamlit interface is temporary.

The final product will consist of:

* A premium Next.js marketing website with multiple animated landing sections inspired by modern SaaS products.
* A dedicated authenticated application workspace for due diligence.
* A scalable Python API powering the frontend.
* A professional SaaS platform suitable for subscription by investment firms.

The backend should continue evolving independently so it can later support web, desktop, or API clients without major architectural changes.
