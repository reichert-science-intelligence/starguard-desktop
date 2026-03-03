# Mobile StarGuard AI — Testing Checklist

Use this to validate the app on **iOS Safari** and **Android Chrome** before demos or portfolio use.

---

## Before you start

- [ ] App runs with `shiny run app.py --host 0.0.0.0`
- [ ] Phone and PC on same Wi‑Fi
- [ ] Opened `http://<your-pc-ip>:8000` on the phone

---

## iOS Safari

| Check | Pass |
|-------|------|
| Page loads without horizontal scroll | ☐ |
| Header and “📱 Mobile Ready” badge visible | ☐ |
| Metric cards stack in one column | ☐ |
| Sidebar opens/closes; nav links ≥44px tap area | ☐ |
| Plotly charts render and are readable | ☐ |
| Sliders/inputs work (ROI by Measure) | ☐ |
| No address bar overlap (safe-area / dvh) | ☐ |
| Rotation portrait ↔ landscape works | ☐ |

**Notes:** If 100vh is short, styles use `100dvh` and `safe-area-inset` where supported.

---

## Android Chrome

| Check | Pass |
|-------|------|
| Page loads without horizontal scroll | ☐ |
| Header and “📱 Mobile Ready” badge visible | ☐ |
| Metric cards stack in one column | ☐ |
| Sidebar and nav taps responsive (44px targets) | ☐ |
| Plotly charts render and are readable | ☐ |
| Sliders/inputs work (ROI by Measure) | ☐ |
| No Chrome UI overlapping key content | ☐ |
| Rotation portrait ↔ landscape works | ☐ |

---

## Shared (both platforms)

| Check | Pass |
|-------|------|
| Dashboard KPIs and HEDIS overview load | ☐ |
| ROI by Measure: sliders move, charts update | ☐ |
| Gap Analysis (and HEDIS Calculator if API set) load | ☐ |
| About page and footer visible | ☐ |
| No console errors that block core flows | ☐ |
| 2‑minute recruiter demo path works end‑to‑end | ☐ |

---

## 2‑minute recruiter demo path

1. Open app on phone → show **Dashboard** and **📱 Mobile Ready** badge.
2. **ROI by Measure** → move one slider → show chart response.
3. **Gap Analysis** → show confidence / self‑correcting message.
4. **About** → highlight $148M+ and zero PHI.

---

## Troubleshooting

- **Can’t reach app on phone:** Firewall may block port 8000; allow Python or add rule for 8000.
- **Charts tiny or broken:** Ensure Plotly CDN loads (check `app.py` script src).
- **Sidebar text dark:** Sidebar CSS in `app.py` and `www/styles.css` force light inputs on dark background; clear cache and reload.

© 2024–2026 Robert Reichert | StarGuard AI™
