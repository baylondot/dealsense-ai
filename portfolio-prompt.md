COMPONENT: PORTFOLIO MANAGEMENT / PORTFOLIO INTELLIGENCE

You are working on DealSense AI, an AI-powered private-equity due-diligence platform.

IMPORTANT:
This is an EXISTING project with substantial backend functionality.

Do NOT immediately create code.

FIRST inspect the entire existing project and understand the architecture.

Read:

- PROJECT_CONTEXT.md
- ARCHITECTURE.md
- ROADMAP.md

Then inspect the actual source code.

==================================================
1. EXISTING FUNCTIONALITY AUDIT
==================================================

Search the entire project for existing functionality related to:

- portfolio
- portfolios
- portfolio management
- portfolio intelligence
- holdings
- investments
- assets
- companies
- company collections
- watchlists
- company tracking
- monitoring
- alerts
- portfolio risk
- concentration
- diversification

Also inspect existing:

- CompanyAnalysis models
- Company Comparison
- Evidence Engine
- News Intelligence
- scoring
- recommendation
- caching
- pipeline/orchestration
- PDF/reporting
- database-related functionality
- API/application-layer functionality

DO NOT assume portfolio functionality is absent simply because there is no portfolio.py file.

==================================================
2. ABSOLUTE NO-DUPLICATION RULE
==================================================

Before creating ANY:

- model
- class
- function
- service
- repository
- cache
- prompt
- utility
- file

search for equivalent existing functionality.

If it already exists:

DO NOT recreate it.

Reuse or extend it only when necessary.

Do not create competing implementations.

==================================================
3. CORE PURPOSE
==================================================

Portfolio Management should allow users to organize multiple companies into a portfolio and derive portfolio-level intelligence from the existing company intelligence.

The system should answer questions such as:

- What companies are in this portfolio?
- What is the overall portfolio quality?
- What are the strongest and weakest companies?
- What are the major portfolio-level risks?
- Is the portfolio concentrated in one industry?
- Is the portfolio concentrated in one business model?
- Which companies have the strongest acquisition scores?
- Which companies require attention?
- What important news has affected portfolio companies?
- What common risks exist across multiple companies?

==================================================
4. SOURCE OF TRUTH
==================================================

Do NOT create a second CompanyAnalysis system.

Portfolio Management should reference and aggregate the existing company intelligence.

Conceptually:

CompanyAnalysis A
CompanyAnalysis B
CompanyAnalysis C
        ↓
Portfolio
        ↓
Portfolio Intelligence

Reuse existing:

- scores
- recommendations
- signals
- risks
- SWOT
- evidence
- news
- company metadata

Do not duplicate these structures unless the existing architecture genuinely requires a portfolio-specific representation.

==================================================
5. PORTFOLIO MODEL
==================================================

Only create a Portfolio model if one does not already exist.

The model should represent a collection of companies.

Conceptually it may contain:

- portfolio ID
- portfolio name
- description
- company references
- created date
- updated date

Adapt this to the project's existing conventions.

Do NOT blindly implement this structure.

==================================================
6. PORTFOLIO COMPANY MEMBERSHIP
==================================================

A portfolio should be able to contain multiple companies.

At minimum support:

- adding a company
- removing a company
- listing companies
- retrieving portfolio information

Do not duplicate CompanyAnalysis data unnecessarily.

Prefer references/relationships to existing company records where the architecture supports this.

==================================================
7. PORTFOLIO METRICS
==================================================

Calculate portfolio-level metrics from existing company data.

Potential metrics:

- number of companies
- average acquisition score
- highest acquisition score
- lowest acquisition score
- average risk level
- number of high-risk companies
- number of SaaS companies
- number of B2B companies
- number of B2C companies
- recurring-revenue exposure
- AI-company exposure
- enterprise exposure
- geographic concentration

Only implement metrics supported by the existing models.

Do NOT invent unavailable data.

==================================================
8. RISK AGGREGATION
==================================================

Aggregate existing company risks.

Example:

Company A:
- regulatory risk

Company B:
- regulatory risk

Company C:
- competition risk

Portfolio-level output:

Regulatory Risk:
2 companies affected

Competition Risk:
1 company affected

Do NOT invent portfolio risks that are not supported by the underlying company analyses.

==================================================
9. CONCENTRATION ANALYSIS
==================================================

Identify concentration across supported dimensions such as:

- industry
- business model
- SaaS
- B2B/B2C
- geography
- recurring revenue
- AI exposure
- enterprise exposure

Example:

5 portfolio companies

4 are SaaS.

The system may identify:

"SaaS concentration is high."

Do not invent numerical thresholds without first inspecting the existing architecture.

If thresholds are needed, define them explicitly and document them.

==================================================
10. COMPANY RANKING
==================================================

Reuse the existing acquisition scoring system.

Do NOT create a second acquisition scoring algorithm.

Portfolio companies may be ranked by:

- acquisition score
- risk
- other existing deterministic metrics

The ranking must use existing structured data.

==================================================
11. NEWS INTELLIGENCE
==================================================

News Intelligence already exists.

DO NOT recreate it.

Portfolio Management should consume existing News Intelligence results.

Conceptually:

Portfolio
    ↓
Portfolio Companies
    ↓
Existing News Intelligence
    ↓
Portfolio News Feed

Do not create another news-search engine.

==================================================
12. EVIDENCE
==================================================

The existing Evidence Engine must remain the source of evidence.

Do NOT create another evidence format.

Portfolio-level claims should be traceable to the underlying company evidence where applicable.

Never:

- fabricate quotes
- fabricate sources
- fabricate URLs
- fabricate evidence

==================================================
13. COMPARISON INTEGRATION
==================================================

Company Comparison already exists.

Do NOT recreate comparison functionality.

Portfolio Management may use existing Company Comparison functionality when appropriate.

For example:

Portfolio companies can be ranked or compared using the existing comparison capabilities.

Do not create a second comparison engine.

==================================================
14. NO AUTOMATIC PDF GENERATION
==================================================

Portfolio Management must NOT automatically generate PDFs.

Do NOT write files into reports/ during ordinary portfolio operations.

Correct behavior:

Portfolio analysis
    ↓
Structured PortfolioResult

Only if the user explicitly requests:

Create Portfolio Report

    ↓
Existing PDF Generator

==================================================
15. NO UNINTENDED SIDE EFFECTS
==================================================

Creating or viewing a portfolio must NOT:

- automatically analyze every company
- automatically generate PDFs
- modify CompanyAnalysis
- modify acquisition scores
- modify recommendations
- overwrite evidence
- overwrite news
- create duplicate cache systems
- change unrelated UI behavior

Portfolio operations should be explicit.

==================================================
16. CACHING
==================================================

Inspect the existing cache system.

If portfolio caching is necessary, integrate with the existing architecture.

Do NOT create a separate unrelated caching framework.

==================================================
17. LLM USAGE
==================================================

Prefer deterministic calculations for:

- counts
- averages
- rankings
- concentration
- risk aggregation
- score aggregation

Use the existing LLM only where semantic synthesis is genuinely useful.

For example:

"Summarize the major investment concerns across this portfolio."

Any LLM-generated result must be structured and validated.

The LLM must not override deterministic calculations.

==================================================
18. ERROR HANDLING
==================================================

Handle:

- nonexistent portfolio
- empty portfolio
- duplicate company
- invalid company reference
- missing company analysis
- incomplete data

Do not fabricate missing information.

Do not silently convert missing information into false.

==================================================
19. TESTING
==================================================

Before declaring completion, test:

1. Create portfolio.

2. Add two companies.

3. Add three or more companies.

4. Remove company.

5. Retrieve portfolio.

6. Calculate portfolio metrics.

7. Calculate risk aggregation.

8. Calculate concentration.

9. Rank companies.

10. Integrate existing News Intelligence.

11. Integrate existing Evidence.

12. Verify Company Comparison is reused rather than duplicated.

13. Verify no PDF is generated automatically.

14. Verify no files are unexpectedly created in reports/.

15. Verify existing CompanyAnalysis still works.

16. Verify existing scoring still works.

17. Verify existing recommendation still works.

18. Verify existing News Intelligence still works.

19. Verify existing PDF generation still requires explicit invocation.

==================================================
20. REGRESSION TESTING
==================================================

After implementation, run the existing core workflows.

Confirm:

Company Analysis
→ works

Company Comparison
→ works

News Intelligence
→ works

PDF generation
→ works only when explicitly requested

Portfolio Management
→ works independently

No existing functionality should regress.

==================================================
21. FILE MODIFICATION RULE
==================================================

Before coding determine exactly which files require modification.

At the end report:

FILES CREATED:
...

FILES MODIFIED:
...

FILES NOT TOUCHED:
...

For every modified file explain why it was necessary.

==================================================
22. NO DEAD CODE
==================================================

Every new function/class/module must have a real purpose and call path.

Do not create:

- placeholders
- unused helpers
- duplicate utilities
- speculative abstractions
- dead code

==================================================
23. DO NOT OVERENGINEER
==================================================

Build only the portfolio capability required by the current architecture.

Do not introduce:

- unnecessary databases
- unnecessary frameworks
- unnecessary microservices
- unnecessary APIs
- unnecessary abstractions

==================================================
24. FINAL REPORT
==================================================

When finished report:

1. Existing portfolio functionality discovered.

2. Duplication audit.

3. Existing functionality reused.

4. New functionality created.

5. Files created.

6. Files modified.

7. Data flow.

8. Tests performed.

9. Regression test results.

10. Example portfolio output.

11. Known limitations.

Do NOT simply say "Done."

IMPORTANT:

Do not rebuild working components.

Do not create duplicate intelligence engines.

Do not create duplicate CompanyAnalysis, Comparison, Evidence, News, Scoring, Recommendation, or PDF systems.

Do not introduce automatic side effects.

Do not declare the component complete until it has been tested against the existing DealSense architecture.