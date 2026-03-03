# 📱 StarGuard AI Mobile — Start Here

**Production-grade mobile Shiny for Python demo.** Get running in 3 minutes.

---

## 1. Install dependencies

```bash
cd starguard-shiny
pip install -r requirements.txt
```

## 2. Run the app

**Option A — Local only (quick check)**  
```bash
shiny run app.py
```
Open **http://127.0.0.1:8000** in your browser.

**Option B — Network (test on your phone)**  
```bash
shiny run app.py --host 0.0.0.0
```
On your **iPhone or Android**, open: `http://<YOUR-PC-IP>:8000`  
(Find your IP: Windows `ipconfig`, Mac/Linux `ifconfig` or `ip addr`.)

**Option C — Use the deploy script (Windows)**  
```cmd
deploy.bat
```
Choose option 2 for network access, then open the URL on your phone.

## 3. What to try

- **Dashboard** — KPIs, HEDIS overview, 📱 Mobile Ready badge.
- **ROI by Measure** — Sliders and charts (touch-friendly).
- **Gap Analysis** — Self-correcting AI / compound engineering.
- **HEDIS Calculator** — 12-measure self-correcting logic.

---

## Next

- **Deployment & mobile testing:** [QUICKSTART.md](QUICKSTART.md)  
- **Full docs & architecture:** [README.md](README.md)  
- **iOS/Android checklist:** [MOBILE_TESTING_CHECKLIST.md](MOBILE_TESTING_CHECKLIST.md)

© 2024–2026 Robert Reichert | StarGuard AI™
