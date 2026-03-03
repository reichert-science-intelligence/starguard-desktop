# Compound Engineering — Technical Architecture

This document describes the **compound engineering** patterns used in StarGuard AI Mobile: self-correcting validation, agentic RAG-style flows, and context engineering for Medicare Advantage / HEDIS.

---

## 1. Self-correcting AI validation

**Idea:** The system generates an answer, validates it against domain rules and historical data, and if needed corrects or flags it — reducing reliance on unreviewed model output.

**Where it appears in the app:**

- **Gap Analysis:** User sets measure, projected close %, and timeline. The backend:
  - Generates recommendations (e.g. from historical closure rates or optional LLM).
  - Validates against historical bands (e.g. typical closure % for that measure).
  - Can adjust confidence or suggest a “corrected” timeline/percentage.
  - Presents a single “validation summary” and optional “correction” message.

- **HEDIS Calculator (12 measures):** User inputs or selections are validated against HEDIS logic and plan context. If values are out of range or inconsistent, the system can:
  - Replace or clamp values to valid ranges.
  - Recompute and surface a “corrected” result with an audit-friendly explanation.

**Benefits:** Fewer bad numbers in front of users; QA time can drop when these checks are in the critical path. Suitable for regulated (e.g. healthcare) demos.

---

## 2. Agentic RAG-style flows

**Idea:** “Retrieval” (e.g. HEDIS specs, historical interventions, measure definitions) plus “generation” (recommendations, narratives) in a loop: the app uses context to produce answers and can re-query or re-validate.

**Where it appears:**

- **Gap Analysis / HEDIS Calculator:** Context (measure, plan size, prior rates) is assembled; recommendations or scores are generated; confidence is derived from how well the suggestion matches retrieved norms (e.g. historical closure rates). Optional LLM calls use this same context for natural-language summaries.

- **Session context:** `compound_framework/session_context.py` (and related session state) keep measure, plan, and user choices in one place so that every “agent” step (validate, correct, recommend) is context-aware.

**Differentiation:** Not a single one-shot prompt; the flow is “context → generate → validate/correct → present,” which aligns with agentic RAG narratives in technical interviews.

---

## 3. Context engineering (Medicare Advantage / HEDIS)

**Idea:** The app is built with **domain context** baked in: HEDIS measure codes, CMS weightings, typical closure ranges, and plan-size assumptions. This improves both self-correction and RAG-style retrieval.

**Where it appears:**

- **HEDIS schemas / measure lists:** `compound_framework/hedis_schemas.py` and the 12-measure HEDIS Calculator define measures and rules.
- **Plan context:** `utils/plan_context.py` (or equivalent) provides plan size and related assumptions used in ROI and gap logic.
- **Financial impact:** `compound_framework/financial_impact.py` uses CMS and plan context to compute revenue impact, ROI, and net benefit.

**Talking point:** “Context engineering” here means the model (or rule engine) isn’t generic — it’s given structured MA/HEDIS context so outputs are relevant and easier to validate.

---

## 4. Audit trails and compliance

**Idea:** For regulated demos, key actions (e.g. “corrected value,” “confidence downgraded”) can be logged so that the “compound” behavior is explainable.

**Where it appears:**

- Session or validation logs (e.g. in `compound_framework` or server logic) can record: input params, validation result, correction (if any), and confidence.
- Optional: export or in-app “Audit” stub that surfaces a simplified trail for demo purposes.

---

## 5. How this fits the mobile app

- **Mobile-first UI** (viewport, touch targets, Mobile Ready badge) is the **delivery layer**.
- **Compound engineering** (self-correcting validation, agentic RAG patterns, context engineering) is the **logic layer** that makes the demo technically sophisticated and different from a static tutorial.
- Together they support a **2‑minute recruiter demo** and a **technical deep-dive** (this doc) for decision makers.

---

## 6. File reference

| Area | Files |
|------|--------|
| Self-correcting / validation | Gap Analysis server logic, HEDIS Calculator, `compound_framework` |
| Session / context | `compound_framework/session_context.py`, `session_memory.json` |
| HEDIS domain | `compound_framework/hedis_schemas.py`, 12-measure list in `app.py` |
| Financial impact | `compound_framework/financial_impact.py`, `utils/roi_calculator.py` |
| UI | `app.py`, `modules/shared_ui.py`, `www/styles.css` |

---

© 2024–2026 Robert Reichert | StarGuard AI™
