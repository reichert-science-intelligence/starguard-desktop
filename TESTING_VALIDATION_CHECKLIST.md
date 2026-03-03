# Testing & Validation Checklist
**StarGuard AI - HEDIS Portfolio Optimizer**

---

## Week 1 Deliverables

| Item | Status | Notes |
|------|--------|-------|
| Sentiment corpus created (1000+ records) | ✅ | `data/sentiment_corpus.csv` - 1,000 records |
| SDoH mapping operational (500+ ZIPs) | ✅ | `data/sdoh_mapping.csv` - 500 ZIPs |
| Sentiment analyzer shows CAHPS risk distribution | ✅ | Sentiment Analysis page under INTELLIGENCE |
| High-risk member list exports successfully | ✅ | Export High-Risk Members to CSV button |
| Cost estimates calculate correctly | ✅ | Disenrollment risk + $1,800 estimated loss |

---

## Week 2 Deliverables

| Item | Status | Notes |
|------|--------|-------|
| AI message generation works | ✅ | Uses Anthropic Claude; requires `ANTHROPIC_API_KEY` |
| Channel optimizer recommends correct channels | ✅ | SMS/Phone/Email/Mail by propensity |
| Portfolio scenarios show ROI calculations | ✅ | Run Scenario → waterfall + value boxes |
| Executive summary aggregates metrics | ✅ | ROI Calculator page - Executive Summary card |
| All modules integrate into single app | ✅ | Sidebar nav: Sentiment, SDoH, Channel, Agentic, Scenarios |

---

## Integration Notes

- **Architecture:** Single `app.py` with sidebar navigation (not navbar + tabs)
- **Data:** `utils/data_loader.py` - sentiment, SDoH, member data (synthetic fallback)
- **Modules:** Content functions + inline server logic (not Shiny `@module` pattern)
- **Executive Summary:** ROI Calculator → Executive Summary card with 3 value boxes

---

## Quick Test Steps

1. **Sentiment:** INTELLIGENCE → Sentiment Analysis → set Risk Threshold → see distribution + high-risk table
2. **SDoH:** INTELLIGENCE → SDoH Barriers → view scatter + barrier summary
3. **Channel:** OPERATIONS → Channel Optimizer → view chart + top members → Download Campaign Plan
4. **Agentic:** OPERATIONS → AI Outreach → select member, tone, Generate Message (needs API key)
5. **Scenarios:** OPERATIONS → Portfolio Scenarios → set target, strategy → Run Scenario
6. **Executive Summary:** FINANCIAL ANALYSIS → ROI Calculator → top card shows $2.3M / $680K / 92%
