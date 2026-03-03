# Side-by-Side Comparison: Streamlit vs Shiny

## 🚀 Both Apps Running

### URLs
- **Streamlit:** http://localhost:8501
- **Shiny:** http://localhost:8502

### How to View Side-by-Side

**Chrome/Edge:**
1. Open both URLs in separate tabs
2. Right-click the Streamlit tab → "Move tab to new window"
3. Press `Win + Left Arrow` to snap Streamlit window to left half
4. Press `Win + Right Arrow` to snap Shiny window to right half

**Firefox:**
1. Open both URLs in separate tabs
2. Drag one tab out to create a new window
3. Use `Win + Left/Right` to snap windows

**Result:**
- **Left:** Streamlit app (port 8501)
- **Right:** Shiny app (port 8502)

---

## 📊 File Count Comparison

| Metric | Streamlit | Shiny | Improvement |
|--------|-----------|-------|-------------|
| **Python Files (pages/)** | 23 files | 5 files | **78% reduction** |
| **CSS Files** | 22+ blocks | 1 file | **95% reduction** |
| **CSS Blocks** | Embedded in each page | Single shared file | **Consolidated** |
| **Entry Point** | app.py + 23 pages | app.py (single file) | **Simplified** |

### Detailed Breakdown

**Streamlit Project:**
- `app.py` - Main entry point
- `pages/` folder - 23 Python files (22 pages + `__init__.py`)
- CSS blocks - Embedded in each page file (22+ separate `<style>` blocks)

**Shiny Project:**
- `app.py` - Main entry point (handles all pages)
- `modules/shared_ui.py` - Reusable UI components
- `www/styles.css` - Single shared stylesheet
- `data/db.py` - Database connection layer

---

## ✅ Feature Comparison

| Feature | Streamlit (8501) | Shiny (8502) |
|---------|-----------------|--------------|
| **Home page loads** | ✅ Yes | ✅ Yes |
| **Metrics display** | ✅ Yes | ✅ Yes |
| **Sidebar nav** | ✅ Yes | ✅ Yes |
| **Purple branding** | ✅ Yes | ✅ Yes |
| **Mobile works** | ⚠️ Sometimes | ✅ Yes |
| **iOS Safari** | ❌ Broken | ✅ Works |
| **Page switch speed** | ⏱️ Full reload | ⚡ Instant |
| **CSS consistency** | ⚠️ Per-page | ✅ Single file |
| **Database connection** | ✅ SQLite/PostgreSQL | ✅ SQLite/PostgreSQL |

---

## 🎯 Key Differences

### Architecture
- **Streamlit:** Multi-file architecture (app.py + 23 page files)
- **Shiny:** Single-file architecture with reactive page switching

### CSS Management
- **Streamlit:** CSS duplicated in each page file
- **Shiny:** Single shared CSS file (`www/styles.css`)

### Mobile Support
- **Streamlit:** Requires JavaScript hacks for iOS Safari
- **Shiny:** Native iOS Safari support (dvh units)

### Page Navigation
- **Streamlit:** Full page reload on navigation
- **Shiny:** Instant page switching (no reload)

---

## 📝 Notes

Both apps are running and ready for comparison. The Shiny version demonstrates:
- Cleaner code organization
- Better mobile compatibility
- Faster page navigation
- Single source of truth for styling
