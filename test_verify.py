#!/usr/bin/env python3
"""
StarGuard AI Mobile — pre-deploy verification.
Checks that key files and mobile/compound features exist.
"""

import os
import sys


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    errors = []
    checks = []

    # Core app
    app_py = os.path.join(base, "app.py")
    if os.path.isfile(app_py):
        checks.append("app.py present")
        with open(app_py, encoding="utf-8", errors="ignore") as f:
            content = f.read()
        if "viewport" in content or "viewport-fit" in content:
            checks.append("viewport meta in app")
        else:
            errors.append("app.py: viewport meta not found")
    else:
        errors.append("app.py missing")

    # Styles
    css = os.path.join(base, "www", "styles.css")
    if os.path.isfile(css):
        checks.append("www/styles.css present")
        with open(css, encoding="utf-8", errors="ignore") as f:
            css_content = f.read()
        if "44px" in css_content or "min-height: 44px" in css_content:
            checks.append("Touch target (44px) in CSS")
        if "safe-area-inset" in css_content or "100dvh" in css_content:
            checks.append("iOS Safari fixes in CSS")
    else:
        errors.append("www/styles.css missing")

    # Compound framework
    cf = os.path.join(base, "compound_framework")
    if os.path.isdir(cf):
        checks.append("compound_framework/ present")
    else:
        errors.append("compound_framework/ missing")

    # Shared UI
    shared = os.path.join(base, "modules", "shared_ui.py")
    if os.path.isfile(shared):
        checks.append("modules/shared_ui.py present")
        with open(shared, encoding="utf-8", errors="ignore") as f:
            su = f.read()
        if "create_header" in su and "create_footer" in su:
            checks.append("shared_ui: create_header, create_footer present")
    else:
        errors.append("modules/shared_ui.py missing")

    # Requirements
    req = os.path.join(base, "requirements.txt")
    if os.path.isfile(req):
        checks.append("requirements.txt present")
    else:
        errors.append("requirements.txt missing")

    # Report
    for c in checks:
        print(f"  [OK] {c}")
    for e in errors:
        print(f"  [FAIL] {e}")

    if errors:
        print("\nVerification failed. Fix the items above.")
        sys.exit(1)
    print("\nAll checks passed. Ready for deploy.")
    sys.exit(0)


if __name__ == "__main__":
    main()
