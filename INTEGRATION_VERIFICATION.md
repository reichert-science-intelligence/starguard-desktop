# Step 1: Integration Verification ✅

## Imports (app.py lines 98-102)

```python
from modules.sentiment_analyzer import sentiment_content
from modules.sdoh_mapper import sdoh_content
from modules.channel_optimizer import channel_optimizer_content
from modules.agentic_outreach import agentic_outreach_content
from modules.portfolio_scenario import portfolio_scenario_content
```

**Note:** Uses content functions (not Shiny `@module.ui`). Each module exports a `*_content()` function; server logic lives in app.py.

## Nav Panels (app.py lines 1178-1189)

| Panel ID   | Sidebar Label        | Content Function            |
|------------|----------------------|-----------------------------|
| `sentiment`| 📞 Sentiment Analysis| `sentiment_content()`       |
| `sdoh`     | 🏘️ SDoH Barriers     | `sdoh_content()`            |
| `channel`  | 📣 Channel Optimizer | `channel_optimizer_content()`|
| `agentic`  | ✉️ AI Outreach       | `agentic_outreach_content()`|
| `scenario` | 📊 Portfolio Scenarios| `portfolio_scenario_content()`|

## Data Loading

- **No file upload:** Data loads automatically via `utils/data_loader.py`
- **Sentiment:** `data/sentiment_corpus.csv` (1,000 records)
- **SDoH:** `data/sdoh_mapping.csv` (500 ZIPs)
- **Members:** Synthetic (300 members) when DB lacks `members` table

---

# Step 2: End-to-End Test Checklist

1. **Launch:** `cd starguard-shiny && python -m shiny run app`
2. **Sentiment Analysis** (INTELLIGENCE → Sentiment Analysis)
   - [ ] Histogram + CAHPS bar chart render
   - [ ] High-risk members table shows rows
   - [ ] Export High-Risk Members to CSV works
3. **SDoH Barriers** (INTELLIGENCE → SDoH Barriers)
   - [ ] Scatter heatmap (Transit vs Food Desert) renders
   - [ ] Barrier summary table shows rows
4. **Channel Optimizer** (OPERATIONS → Channel Optimizer)
   - [ ] Cost per Success bar chart renders
   - [ ] Top 100 members with channel recommendations
   - [ ] Download Campaign Plan works
5. **AI Outreach** (OPERATIONS → AI Outreach)
   - [ ] Member dropdown populates (top 50)
   - [ ] Select member → profile displays
   - [ ] Generate Message → returns text (needs ANTHROPIC_API_KEY)
6. **Portfolio Scenarios** (OPERATIONS → Portfolio Scenarios)
   - [ ] Run Scenario → waterfall chart + value boxes
   - [ ] Top targets table shows 50 rows
