---
title: StarGuard Desktop
emoji: ⭐
colorFrom: purple
colorTo: blue
sdk: docker
app_port: 8000
pinned: false
---

# StarGuard AI - Desktop Intelligence Platform

**Production Shiny for Python application** - Migrated from Streamlit (legacy version in git history)

Full-featured Medicare Advantage analytics dashboard optimized for desktop/laptop use.

## 🚀 Features

- **18+ Interactive Pages**: Comprehensive healthcare analytics
- **Wide-screen Layouts**: Optimized for desktop/laptop displays
- **Advanced Visualizations**: Multi-panel dashboards and detailed reporting
- **Professional Portfolio**: Complete About and Services pages
- **Embedded Avatar**: 168KB professional profile integration

## 📊 Key Pages

- **About**: Professional credentials, $148M+ impact, technical architecture
- **Services & Pricing**: Market intelligence, contract rates ($200-350/hr)
- **Analytics Dashboard**: HEDIS, Star Ratings, HCC risk adjustment
- **Predictive Models**: 93% accuracy across 20+ applications

## 🛠️ Tech Stack

- **Framework**: Shiny for Python 0.10.2
- **Language**: Python 3.11
- **Deployment**: HuggingFace Spaces (Docker)
- **Analytics**: Medicare Advantage, HEDIS, Star Ratings

## 🏃 Quick Start

### Run Locally
```bash
# Using run script (recommended)
.\run_starguard_shiny.ps1

# Or manually
shiny run app.py --port 8002
```

Open: http://localhost:8002

### Run via Docker
```bash
docker build -t starguard-desktop .
docker run -p 8000:8000 starguard-desktop
```

## 📁 Project Structure
```
starguard-desktop/
├── app.py                    # Main Shiny application
├── www/                      # Static HTML files
│   ├── starguard_about.html  # About page (168KB with avatar)
│   └── starguard_services.html # Services page (33KB)
├── pages/                    # Analytics pages
├── utils/                    # Helper functions
├── run_starguard_shiny.ps1   # Windows run script
├── Artifacts/
│   └── old-streamlit/        # Legacy Streamlit (archived)
└── README.md
```

## 🎯 Migration Notes

**March 2026**: Migrated from Streamlit to Shiny for Python
- Improved performance and reactivity
- Better mobile responsiveness
- Enhanced UI/UX with modern components
- Professional About & Services integration

Legacy Streamlit code available in git history (pre-migration commits).

## 👨‍💻 Built By

**Robert Reichert** - Healthcare Data Scientist & AI Architect
- 22+ years Medicare Advantage analytics
- $148M+ documented cost savings
- 93% prediction accuracy across 20+ production apps

📧 reichert.starguardai@gmail.com
🔗 [LinkedIn](https://linkedin.com/in/robert-reichert-423023302)
💼 Available March 2026 | Contract Rate: $200-350/hr

## 📱 Related Apps

- **StarGuard Mobile**: https://huggingface.co/spaces/rreichert/starguard-mobile
- **AuditShield**: https://huggingface.co/spaces/rreichert/auditshield-live
- **Landing Page**: https://tinyurl.com/bdevpdz5

## 📝 License

Copyright © 2026 Robert Reichert. All rights reserved.
