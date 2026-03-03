# StarGuard AI Mobile — Quick Start & Deployment

60-second deployment options and mobile testing.

---

## Prerequisites

- Python 3.10+
- `pip install -r requirements.txt` (from `starguard-shiny` folder)

---

## Run options

| Goal | Command | URL |
|------|--------|-----|
| Local only | `shiny run app.py` | http://127.0.0.1:8000 |
| Network (mobile) | `shiny run app.py --host 0.0.0.0` | http://\<your-ip\>:8000 |
| Port 8502 | `shiny run app.py --port 8502` | http://127.0.0.1:8502 |

**Windows:** Use `deploy.bat` and pick an option.  
**Optional:** Set `ANTHROPIC_API_KEY` in `.env` for AI-backed features (Gap Analysis, HEDIS Calculator).

---

## Test on your phone

1. Run with `--host 0.0.0.0`.
2. Find your PC’s IP (e.g. `ipconfig` on Windows).
3. On phone (same Wi‑Fi): open `http://192.168.x.x:8000`.
4. Confirm: layout, taps, charts, and sidebar all work.

See [MOBILE_TESTING_CHECKLIST.md](MOBILE_TESTING_CHECKLIST.md) for iOS Safari and Android Chrome checks.

---

## Deploy to shinyapps.io (optional)

1. Install RSConnect: `pip install rsconnect-python`
2. Configure: `rsconnect add --account <your-account> --name shinyapps`
3. Deploy: `rsconnect deploy shiny . --name starguard-mobile`
4. Share the generated URL (HTTPS, works on mobile).

---

## File summary

- **app.py** — Main Shiny app (mobile-first, compound engineering).
- **www/styles.css** — Responsive breakpoints, touch targets, Mobile Ready badge.
- **compound_framework/** — Self-correcting AI, session context, HEDIS schemas.
- **START_HERE.md** — This path; **README.md** — Full technical docs.

© 2024–2026 Robert Reichert | StarGuard AI™
