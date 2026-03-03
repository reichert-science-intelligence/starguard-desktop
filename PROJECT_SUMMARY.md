# StarGuard AI Mobile — Project Summary

One-page overview for recruiters and technical decision makers.

---

## What it is

**Production-grade mobile Shiny for Python demo:** HEDIS portfolio optimizer with compound engineering (self-correcting AI, agentic RAG-style flows), mobile-first UI, and cross-platform validation (iOS Safari + Android Chrome). Built to showcase technical depth and differentiate from tutorial-style projects.

---

## Phases delivered

| Phase | Content |
|-------|--------|
| **1. Foundation** | Mobile-responsive framework: viewport meta, 44px touch targets, breakpoints 320px–2560px, iOS safe-area/dvh, 📱 Mobile Ready badge |
| **2. Compound engineering** | Self-correcting validation (Gap Analysis, HEDIS Calculator), session context, HEDIS schemas, financial impact logic |
| **3. Cross-platform** | MOBILE_TESTING_CHECKLIST.md for iOS Safari and Android Chrome; tested layout and touch behavior |
| **4. Polish & badge** | Mobile Ready badge in UI, START_HERE / QUICKSTART / README, COMPOUND_ENGINEERING.md, SCREENSHOT_GUIDE.md |

---

## Tech stack

- **Shiny for Python** — App framework
- **Plotly** — Charts (mobile-responsive)
- **Pandas / NumPy** — Data
- **Optional:** Anthropic API for AI-backed Gap / HEDIS flows
- **CSS:** Custom mobile-first styles (no Bootstrap dependency)

---

## Key differentiators

- **Compound engineering:** Generate → validate → correct flows; agentic RAG-style context; Medicare Advantage / HEDIS context engineering.
- **Mobile-first:** One codebase for desktop and phone; touch-optimized; Mobile Ready certification narrative.
- **Documented impact:** $148M+ savings, zero PHI exposure, HIPAA-first positioning for demos.

---

## File map

- **app.py** — Main Shiny app (viewport, badge, nav, all pages)
- **www/styles.css** — Mobile-first CSS, touch targets, badge, iOS fixes
- **compound_framework/** — Self-correcting logic, session context, HEDIS schemas, financial impact
- **modules/shared_ui.py** — Header, cards, security badge, **mobile_ready_badge**
- **START_HERE.md** — 3-minute run path
- **QUICKSTART.md** — Deployment options
- **README.md** — Full project docs
- **MOBILE_TESTING_CHECKLIST.md** — iOS/Android validation
- **COMPOUND_ENGINEERING.md** — Architecture deep dive
- **SCREENSHOT_GUIDE.md** — Portfolio/LinkedIn screenshots
- **deploy.bat / deploy.sh** — Run with local or network access
- **test_verify.py** — Pre-deploy checks

---

## How to run

```bash
pip install -r requirements.txt
shiny run app.py
# Or: shiny run app.py --host 0.0.0.0   (then open http://YOUR-IP:8000 on phone)
# Or: deploy.bat (Windows) / ./deploy.sh (Bash)
```

---

## Demo talking points

- **Recruiters (2 min):** “This mobile demo shows compound engineering: self-correcting validation, agentic RAG patterns, and production mobile UX. Built for Medicare Advantage–style use cases with documented impact.”
- **Technical:** “Three patterns: self-correcting validation loops, agentic RAG with confidence scoring, and context engineering for MA/HEDIS. Production AI with audit-friendly behavior.”
- **Healthcare:** “HEDIS Star Rating optimization with intervention prioritization and ROI — all on mobile, cross-platform validated.”

---

© 2024–2026 Robert Reichert | StarGuard AI™
