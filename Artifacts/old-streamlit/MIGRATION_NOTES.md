# Legacy Streamlit Archive

**March 2026 Migration**: This folder was reserved for the legacy Streamlit version.

The previous Streamlit codebase is preserved in the git history. To recover it:

```bash
# View the commit before the Shiny migration
git log --oneline

# Checkout the old Streamlit version (replace <commit> with the pre-migration hash)
git show <commit>:app.py
# Or restore the full tree:
git archive <commit> -o old-streamlit-backup.zip
```

The migration replaced Streamlit with Shiny for Python for improved performance, reactivity, and UI/UX.
