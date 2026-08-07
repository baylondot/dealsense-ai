# DealSense AI — Project Context & Engineering Instructions

You are joining an existing software project called **DealSense AI**. Your job is to continue building it as a senior software engineer while preserving the existing architecture and avoiding unnecessary refactors.

---

# Project Vision

DealSense AI is an AI-powered Due Diligence platform for Private Equity, Venture Capital, M&A advisors, Investment Banks, and Acquisition firms.

The goal is to allow a user to enter a company website and receive a professional investment-grade analysis that includes research, risk assessment, acquisition scoring, and actionable recommendations.

This should eventually feel like a modern SaaS platform that firms could genuinely subscribe to—not a student project or a demo.

The long-term objective is to produce software comparable in quality, polish, and usability to products used by firms like Pocket Fund.

---

# Current Backend

The backend already exists and should be treated as the source of truth.

Current architecture includes modules such as:

* app.py
* analysis.py
* pipeline.py
* scraper.py
* research.py
* tavily_search.py
* llm.py
* prompts.py
* models.py
* scoring.py
* recommendation.py
* cache.py
* constants.py

The project currently uses:

* Python
* Streamlit (temporary frontend)
* OpenRouter
* Google Gemini models through OpenRouter
* Jina AI Reader
* Tavily Search
* Pydantic
* JSON structured outputs

Do not recreate these files or duplicate their responsibilities.

Always inspect the existing implementation before suggesting changes.

---

# Engineering Rules

Follow these principles throughout development.

## 1. Never invent architecture

If a function or module does not exist, do not assume it exists.

Inspect the codebase before proposing changes.

Never ask the user to recreate already existing functionality.

---

## 2. Single Responsibility Principle

Each module should have one clear responsibility.

Examples:

* scraper.py → obtain website HTML
* research.py → clean and prepare research
* tavily_search.py → external research
* analysis.py → AI analysis only
* scoring.py → scoring only
* recommendation.py → recommendations only
* pipeline.py → orchestration only

---

## 3. Backward Compatibility

Never break existing working code.

When introducing improvements:

* extend
* refactor carefully
* preserve existing functionality

Avoid large breaking changes.

---

## 4. Production Quality

Avoid temporary fixes.

Avoid hacks.

Avoid duplicated logic.

Prefer maintainable solutions over quick ones.

---

## 5. Think Like a Startup

Assume this project will become a commercial SaaS product.

Every decision should scale.

---

# Planned Backend Roadmap

Continue implementing professional PE features including:

* Better acquisition scoring
* Evidence engine
* Source attribution
* Company comparison
* Portfolio analysis
* Investment memo generation
* PDF exports
* Research history
* News intelligence
* Multi-source research
* Better caching
* API endpoints
* Authentication
* Database support
* Usage analytics

Prefer adding capabilities instead of repeatedly reorganizing architecture.

---

# Frontend Vision (Extremely Important)

The current Streamlit UI is temporary.

The final frontend should be built using a modern JavaScript framework (preferably React + Next.js) while keeping the Python backend intact.

The frontend should feel like a premium SaaS product launched in 2026.

It must NOT resemble:

* legacy banking software
* enterprise software from the early 2000s
* school management systems
* CRUD dashboards with basic tables

Instead, the inspiration should come from companies such as:

* Vercel
* Linear
* Stripe
* Notion
* Arc Browser
* Raycast
* Framer
* Clerk
* Supabase

The visual quality should be high enough that users immediately perceive it as a premium commercial platform.

---

# Landing Experience

The landing experience should be a storytelling website rather than a dashboard.

Approximately 6–8 full-screen sections should appear while scrolling.

Examples of sections:

1. Hero
2. Product Overview
3. AI Research Engine
4. Due Diligence Features
5. Acquisition Intelligence
6. Workflow Demonstration
7. Testimonials / Trust
8. Pricing / Call to Action

Each section should use smooth transitions.

Preferred interactions include:

* fade-in
* fade-out
* slide
* subtle parallax
* staggered animations
* animated cards
* animated graphs
* responsive illustrations
* elegant motion
* modern typography

Animations should enhance usability rather than distract.

The experience should feel similar to premium SaaS marketing sites.

---

# Application Workspace

After clicking "Start Analysis" or "Go to Analyze", users should enter a completely different interface.

This workspace should be focused, distraction-free, and productivity-oriented.

Think of products like:

* Linear
* Notion
* Cursor
* Vercel Dashboard

The workspace should prioritize clarity over decoration.

---

# Analysis Dashboard

The analysis page should display information using modern cards and layouts rather than long paragraphs.

Possible sections include:

* Executive Summary
* Business Model
* Products
* Customers
* Competitors
* SWOT
* Investment Signals
* Risks
* Acquisition Score
* Recommendation
* Evidence
* Sources

Cards should automatically adapt to screen size.

Avoid dense tables whenever possible.

---

# Responsiveness

The interface must work well on:

* Desktop
* Laptop
* Tablet
* Mobile

Animations should remain smooth across screen sizes.

---

# Design Philosophy

Less clutter.

More whitespace.

Elegant typography.

Rounded corners.

Subtle shadows.

Professional color palette.

Fluid motion.

Responsive layouts.

High-quality icons.

Meaningful micro-interactions.

The UI should communicate trust and professionalism suitable for financial decision-making.

---

# Development Workflow

Before making architectural changes:

1. Read the existing implementation.
2. Understand current responsibilities.
3. Extend rather than replace.
4. Explain why a change is needed.

Never suggest rebuilding working modules unnecessarily.

---

# Goal

By the end of development, DealSense AI should look and feel like a venture-backed SaaS platform that a Private Equity firm could confidently adopt, while maintaining clean architecture, production-quality engineering, and an exceptional user experience.
