"""
Compound Framework - Day 3-4: Session Learning Context

Accumulates what works across Claude sessions. Inject into prompts for consistent outputs.
"""
import json
import os
from datetime import datetime


class SessionLearningContext:
    """Accumulates what works across Claude sessions"""

    def __init__(self, memory_file: str = None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.memory_file = memory_file or os.path.join(base_dir, "session_memory.json")
        self.successful_patterns = []
        self.failed_approaches = []

        # Domain knowledge (HEDIS MY2025, 12-measure portfolio)
        self.domain_constraints = {
            "HEDIS_measures": [
                "GSD", "KED", "EED", "PDC-DR", "BPD",  # Tier 1: Diabetes
                "CBP", "SUPD", "PDC-RASA", "PDC-STA",   # Tier 2: Cardiovascular
                "BCS", "COL", "HEI"                     # Tier 3: Cancer; Tier 4: Equity
            ],
            "date_logic": "measurement_year ends Dec 31; lookback varies by measure (e.g. BCS 27mo, COL 10yr)",
            "PHI_safe": "Never display member_id, SSN, or DOB in output",
            "Star_Rating_weights": {
                "GSD": 3,
                "KED": 3,
                "CBP": 3,
                "BCS": 1,
                "COL": 1,
            }
        }

        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.successful_patterns = data.get("successful", [])
                    self.failed_approaches = data.get("failed", [])
            except (json.JSONDecodeError, IOError):
                pass

    def inject_context(self, user_prompt: str) -> str:
        """Prepend learned patterns to Claude requests"""

        context_header = f"""
## Auto-Injected Session Context (From Previous Successful Runs)

**Domain Rules (Always Apply):**
{json.dumps(self.domain_constraints, indent=2)}

**Previously Successful Patterns (Reuse These):**
{self._format_successes()}

**Known Failures (Avoid These):**
{self._format_failures()}

---
**Current User Request:**
{user_prompt}
"""
        return context_header

    def _format_successes(self) -> str:
        if not self.successful_patterns:
            return "No successful patterns yet (this is your first run)"
        return "\n".join([
            f"- {p['approach'][:100]}... (accuracy: {p['accuracy']:.2%})"
            for p in self.successful_patterns[-5:]
        ])

    def _format_failures(self) -> str:
        if not self.failed_approaches:
            return "No failures yet"
        return "\n".join([
            f"- {f.get('error', '')[:80]}..."
            for f in self.failed_approaches[-3:]
        ])

    def record_outcome(self, approach: str, success: bool, accuracy: float = 0.0, error: str = None):
        """Save what worked (or didn't) for next time"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "approach": approach,
            "accuracy": accuracy
        }
        if success:
            self.successful_patterns.append(entry)
        else:
            entry["error"] = error or ""
            self.failed_approaches.append(entry)
        self._save_memory()

    def _save_memory(self):
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump({
                "successful": self.successful_patterns,
                "failed": self.failed_approaches
            }, f, indent=2)


if __name__ == "__main__":
    ctx = SessionLearningContext()
    print("SessionLearningContext imported OK")
    print("Domain measures:", ctx.domain_constraints["HEDIS_measures"])
