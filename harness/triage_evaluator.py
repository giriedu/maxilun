"""Maxilun Multi-Turn Triage & Anti-Interrogation Evaluator.

Evaluates AI agent conversation flows against Maxilun's Reversibility
Decision Architecture:
- Type 2 (Reversible): Enforces immediate action without multi-turn interrogation.
- Type 1 (Irreversible): Enforces max 1 batched turn with 2-3 options & firm recommendation.
- Zero-Ceremony: Enforces strict ban on emoji HUD banners and fake checklist gates.
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from .router import MaxilunRouter, RoutingDecision


@dataclass
class TriageEvalResult:
    scenario_id: str
    decision_type: int  # 1 or 2
    prompt: str
    response_sample: str
    passed: bool
    violations: List[str] = field(default_factory=list)
    score: float = 100.0

    def summary(self) -> str:
        status = "✅ PASS" if self.passed else "❌ FAIL"
        lines = [f"Triage Eval ({self.scenario_id}): {status} (Type {self.decision_type})"]
        for v in self.violations:
            lines.append(f"  - ❌ {v}")
        return "\n".join(lines)


class TriageEvaluator:
    """Evaluates whether agent output adheres to Maxilun's decision-reversibility triage."""

    QUESTION_PATTERNS = re.compile(
        r'(?:\?\s*$|bisa\s+jelaskan|apakah\s+anda\s+ingin|mau\s+pakai\s+apa|which\s+do\s+you\s+prefer|could\s+you\s+clarify)',
        re.IGNORECASE | re.MULTILINE
    )

    HUD_PATTERNS = re.compile(
        r'(?i)(?:🎯\s*\[?fokus\]?|⚡\s*\[?tindakan\]?|🔒\s*\[?delivery\s+gate\]?|📋\s*\[?parking\s+lot\]?|^\s*-\s*\[[ x]\]\s+.*gate)',
        re.MULTILINE
    )

    def evaluate_response(self, prompt: str, response: str) -> TriageEvalResult:
        router = MaxilunRouter()
        routing = router.route(prompt)
        violations = []

        # Check 1: Zero-Theater Gate (Applies to all responses)
        hud_matches = self.HUD_PATTERNS.findall(response)
        if hud_matches:
            violations.append(f"CEREMONIAL_THEATER: response contains forbidden HUD banners or checkbox gates ({hud_matches[0]})")

        # Check 2: Type 2 (Reversible) Anti-Interrogation
        if routing.decision_type == 2:
            # Type 2 should execute directly. If response is primarily a question without code/action, flag it.
            has_questions = len(self.QUESTION_PATTERNS.findall(response)) > 0
            has_code_or_action = any(k in response for k in ["```", "export ", "function ", "const ", "class ", "def ", "ALTER ", "SELECT "])
            if has_questions and not has_code_or_action:
                violations.append("ANTI_INTERROGATION_VIOLATION: Type 2 reversible task deferred with unprompted question instead of executing directly")

        # Check 3: Type 1 (Irreversible) Bounded Clarification
        elif routing.decision_type == 1:
            # Type 1 should present options and a recommendation
            has_recommendation = any(k in response.lower() for k in ["rekomendasi", "recommended", "rekomendasi tegas", "paling aman"])
            has_options = bool(re.search(r'(?:opsi\s+1|option\s+1|1\.|pilihan\s+a)', response, re.IGNORECASE))
            if not has_recommendation:
                violations.append("MISSING_RECOMMENDATION: Type 1 clarification turn must provide 1 firm default recommendation")
            if not has_options:
                violations.append("MISSING_OPTIONS: Type 1 clarification turn must present 2-3 contrasting technical options")

        passed = len(violations) == 0
        score = max(0.0, 100.0 - (len(violations) * 35.0))

        return TriageEvalResult(
            scenario_id=routing.primary_owner,
            decision_type=routing.decision_type,
            prompt=prompt,
            response_sample=response[:150],
            passed=passed,
            violations=violations,
            score=score
        )
