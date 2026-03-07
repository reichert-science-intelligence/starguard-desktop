# setup_env.py
"""
Automated setup script for StarGuard AI development environment
Installs dependencies, creates .env template, and verifies configuration
"""

import subprocess
import sys
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def run_command(cmd, description):
    """Run a shell command and report status"""
    print(f"-> {description}...")
    try:
        subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        print("  [OK] Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  [FAIL] {e.stderr or str(e)}")
        return False


def create_file_if_not_exists(filepath, content, description):
    """Create a file with content if it doesn't exist"""
    path = Path(filepath)

    if path.exists():
        print(f"-> {description}...")
        print(f"  [SKIP] Already exists: {filepath}")
        return False
    else:
        print(f"-> Creating {description}...")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"  [OK] Created: {filepath}")
        return True


def main():
    print_header("StarGuard AI - Development Environment Setup")

    # Verify we're in the right directory
    if not Path("app.py").exists():
        print(
            "[FAIL] Error: app.py not found. Please run this script from starguard-shiny directory"
        )
        print("  cd starguard-shiny")
        print("  python setup_env.py")
        sys.exit(1)

    print("[OK] Found app.py - proceeding with setup\n")

    # ========================================================================
    # STEP 1: Install python-dotenv
    # ========================================================================
    print_header("Step 1: Installing Dependencies")

    run_command(
        f"{sys.executable} -m pip install python-dotenv>=1.0.0",
        "Installing python-dotenv",
    )

    # ========================================================================
    # STEP 2: Create .env template
    # ========================================================================
    print_header("Step 2: Creating .env Configuration File")

    env_content = """# StarGuard AI Environment Configuration
# ==========================================
# IMPORTANT: This file contains sensitive information and should NEVER be committed to Git

# REQUIRED: Anthropic API Key
# Get your key from: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-api03-REPLACE-WITH-YOUR-ACTUAL-KEY-HERE

# OPTIONAL: Database Configuration (for PostgreSQL production use)
# DB_HOST=localhost
# DB_NAME=starguard
# DB_USER=postgres
# DB_PASSWORD=your-password

# OPTIONAL: Golden Dataset Configuration
# GOLDEN_PLAN_ID=H1234
"""

    env_created = create_file_if_not_exists(".env", env_content, ".env configuration file")

    # ========================================================================
    # STEP 3: Update .gitignore
    # ========================================================================
    print_header("Step 3: Updating .gitignore")

    gitignore_content = """# Environment variables (NEVER commit this)
.env
.env.*

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
logs/
*.log

# Outputs
outputs/
*.pdf
*.csv

# Database
*.db
*.sqlite
*.sqlite3

# OS
.DS_Store
Thumbs.db

# Shiny
.shiny_app_*
rsconnect/
"""

    gitignore_path = Path(".gitignore")
    if gitignore_path.exists():
        content = gitignore_path.read_text()
        if ".env" in content:
            print("-> Checking .gitignore...")
            print("  [OK] .env already excluded in .gitignore")
        else:
            print("-> Updating .gitignore...")
            with open(".gitignore", "a") as f:
                f.write("\n# Added by setup script\n.env\n.env.*\n")
            print("  [OK] Added .env to .gitignore")
    else:
        create_file_if_not_exists(".gitignore", gitignore_content, ".gitignore file")

    # ========================================================================
    # STEP 4: Update requirements.txt
    # ========================================================================
    print_header("Step 4: Updating requirements.txt")

    req_path = Path("requirements.txt")
    if req_path.exists():
        content = req_path.read_text()
        if "python-dotenv" in content:
            print("-> Checking requirements.txt...")
            print("  [OK] python-dotenv already in requirements.txt")
        else:
            print("-> Updating requirements.txt...")
            with open("requirements.txt", "a") as f:
                f.write("\n# Environment variable management\npython-dotenv>=1.0.0\n")
            print("  [OK] Added python-dotenv to requirements.txt")
    else:
        print("  [SKIP] requirements.txt not found")

    # ========================================================================
    # STEP 5: Verify app.py has dotenv loading
    # ========================================================================
    print_header("Step 5: Verifying app.py Configuration")

    app_content = Path("app.py").read_text()
    if "load_dotenv()" in app_content:
        print("-> Checking app.py...")
        print("  [OK] app.py already has dotenv loading")
    else:
        print("-> Checking app.py...")
        print("  [WARN] app.py does NOT have dotenv loading")
        print("\n  Add this at the TOP of app.py:")
        print("\n" + "-" * 70)
        print("""from dotenv import load_dotenv
import os

load_dotenv()

if not os.environ.get("ANTHROPIC_API_KEY"):
    print("WARNING: ANTHROPIC_API_KEY not found - edit .env file")
else:
    print("[OK] API key loaded successfully")
""")
        print("-" * 70 + "\n")

    # ========================================================================
    # FINAL INSTRUCTIONS
    # ========================================================================
    print_header("Setup Complete! Next Steps:")

    if env_created:
        print("[REQUIRED] Edit your API key")
        print("   1. Open: starguard-shiny/.env")
        print("   2. Replace: sk-ant-api03-REPLACE-WITH-YOUR-ACTUAL-KEY-HERE")
        print("   3. With your real key from: https://console.anthropic.com/")
        print()
    else:
        print("[INFO] .env already exists - ensure ANTHROPIC_API_KEY is set")
        print()

    print("[START] Run the application:")
    print("   shiny run app.py")
    print()
    print("[VERIFY] You should see: '[OK] API key loaded successfully'")
    print()
    print("[SECURITY] NEVER commit .env to Git (already in .gitignore)")
    print("   Verify: git status (should NOT show .env)")
    print()

    print_header("Setup Script Finished")


if __name__ == "__main__":
    main()
