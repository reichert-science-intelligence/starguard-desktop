# Phase 1 HEDIS Portfolio Optimizer Enhancement - Week 1 Status

**Implementation Date:** February 11, 2026  
**Status:** Week 1 Complete ✅

---

## ✅ Implemented Components

### Data (Day 1-2)
- **`data/sentiment_corpus.csv`** – 1,000 synthetic call transcripts with CAHPS sentiment scores
- **`data/sdoh_mapping.csv`** – 500 ZIP codes with food desert, transit access, poverty, uninsured rates
- **`data/create_sentiment_corpus.py`** – Script to regenerate sentiment data
- **`data/create_sdoh_mapping.py`** – Script to regenerate SDoH mapping

### Data Loader (Day 2-3)
- **`utils/data_loader.py`** – Loads sentiment corpus, SDoH mapping, and member data
  - `load_sentiment_corpus()` – Returns call transcript DataFrame
  - `load_sdoh_mapping()` – Returns ZIP→SDoH barrier scores
  - `load_member_data_for_outreach()` – DB or synthetic members
  - `get_merged_member_sdoh()` – Members joined with SDoH by ZIP

### Modules (Day 3-7)

#### 1. Sentiment Analyzer (`modules/sentiment_analyzer.py`)
- CAHPS category filter (Getting Care Quickly, Customer Service, Care Coordination, Health Plan Information)
- Risk threshold slider (-1.0 to 0)
- Sentiment distribution histogram + predicted CAHPS impact bar chart
- High-risk members table with disenrollment risk and estimated loss
- Intervention impact recommendations

#### 2. SDoH Mapper (`modules/sdoh_mapper.py`)
- Scatter: Transit Access vs. Food Desert score, colored by HEDIS gap count
- Quadrant lines: High Food Risk (y=6), Low Transit Access (x=5)
- Barrier summary table with recommended interventions (Uber Health, meal delivery, standard outreach)

#### 3. Channel Optimizer (`modules/channel_optimizer.py`)
- Channel efficiency bar chart (Cost per Successful Contact)
- Top 100 members with channel recommendations (SMS, Phone, Email, Mail)
- Download Campaign Plan CSV

### Navigation
- **Sentiment Analysis** – Under INTELLIGENCE
- **SDoH Barriers** – Under INTELLIGENCE
- **Channel Optimizer** – Under OPERATIONS

---

## 📁 File Structure

```
starguard-shiny/
├── data/
│   ├── sentiment_corpus.csv      # Generated
│   ├── sdoh_mapping.csv          # Generated
│   ├── create_sentiment_corpus.py
│   └── create_sdoh_mapping.py
├── modules/
│   ├── sentiment_analyzer.py
│   ├── sdoh_mapper.py
│   └── channel_optimizer.py
├── utils/
│   └── data_loader.py
└── app.py                         # Integrated all three pages
```

---

## 🔄 Regenerating Data

```powershell
cd starguard-shiny
python -m data.create_sentiment_corpus
python -m data.create_sdoh_mapping
```

---

## 📝 Notes

- **Sentiment:** Uses pre-computed scores from synthetic corpus (no live transformers/NLP)
- **SDoH:** Member data uses synthetic fallback when DB lacks `members`/`gaps` tables
- **Channel propensity:** Simple rule-based model (age, tech_savvy, email_on_file)

---

---

## ✅ Week 2: Agentic Outreach & Portfolio Scenarios

### Agentic Outreach (`modules/agentic_outreach.py`)
- Member selection (top 50 from channel propensity)
- Message tone: Empathetic, Urgent, Educational, Incentive-Focused
- AI message generation via Anthropic Claude (claude-3-5-haiku)
- Member profile display (age, gaps, barrier, channel, sentiment)
- Impact analysis (character count, response rate, expected value)
- Requires `ANTHROPIC_API_KEY` in .env

### Portfolio Scenario (`modules/portfolio_scenario.py`)
- Target members slider (100–5000)
- Prioritization: Cost to Close, Highest Gap Count, Star Rating Impact, Disenrollment Risk
- Include SDoH interventions toggle (transport + food barriers)
- Waterfall chart: Intervention Cost → Revenue → Net Impact
- Value boxes: Investment, Revenue, Gaps Closed, Star Lift, ROI
- Top 50 targets data grid
- Run Scenario button triggers computation

### Data Flow
- `_channel_propensity()` now includes `estimated_cost` for scenario engine
- `get_member_sentiment_lookup()` joins sentiment corpus for churn-risk prioritization
- SDoH costs: $50 transport barrier, $30 food barrier; 30% closure rate lift when included

---

**Week 1 + Week 2 Complete** ✅
