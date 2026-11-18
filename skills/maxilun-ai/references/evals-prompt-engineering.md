# Evals & Production Prompt Engineering

Protocol for deterministic testing of LLM systems and for evidence-based evaluation architecture.

---

## 1. Structured Output & JSON Schema Invariants

Do not ask a model for free-form JSON without schema validation:
1. **Schema Enforcement**: Use `response_format: { type: "json_schema", json_schema: { strict: true, ... } }` on the OpenAI provider, or tool call payload validation.
2. **Deterministic Fallbacks**: When JSON parsing fails, run a single repair loop that includes the verbatim syntax error message from the parser (e.g. `json.decoder.JSONDecodeError`).

---

## 2. Prompt Regression Evaluation Framework (Prompt Evals)

Test every system prompt change against a regression test suite of at least 30–50 focused test samples:

| Evaluation Criterion | Measurement Method | Pass Standard |
|---|---|---|
| **Exact Match / Regex** | Static pattern extraction (error codes, status enums, file paths) | 100% deterministic pass |
| **Purity & Grounding** | Purity linter (rejects clichéd AI buzzwords, fake gradients) | Purity score $\ge 95/100$ |
| **Faithfulness / Hallucination** | LLM-as-a-judge: verifies every claim against the context documents | Zero hallucinated assertions |
| **Latency & Token Budget** | p95 latency and completion token count measurement | Below the application SLA target |

---

## 3. LLM-as-a-Judge Evaluation Rubric

When a frontier model (e.g. Claude 3.7 Sonnet / GPT-4o) grades the output of a smaller model:
1. **Give a Clear Binary Rubric**: Grade against concrete criteria (1 = meets, 0 = violates), not a subjective 1–10 scale.
2. **Require an Evidence Quote**: The judge model must include the verbatim sentence that supports its decision before it states the conclusion.

---

## 4. Maxilun Evaluation Quality Cycle (Maxilun Eval Flywheel)

A 5-stage iterative method to measure, evaluate, and raise the quality of language models and autonomous agents:

```
   ┌────────────────────────────────────────────────────────┐
   │  1. Data Preparation (Dataset & Synthetic Scenarios)   │
   └───────────────────────────┬────────────────────────────┘
                               │
                               ▼
   ┌────────────────────────────────────────────────────────┐
   │  2. Inference Run / Multi-Turn Simulation              │
   └───────────────────────────┬────────────────────────────┘
                               │
                               ▼
   ┌────────────────────────────────────────────────────────┐
   │  3. Grading (Binary Rubric + Citation Grounding)       │
   └───────────────────────────┬────────────────────────────┘
                               │
                               ▼
   ┌────────────────────────────────────────────────────────┐
   │  4. Loss Clustering & Failure Pattern Grouping         │
   └───────────────────────────┬────────────────────────────┘
                               │
                               ▼
   ┌────────────────────────────────────────────────────────┐
   │  5. Iterative Remediation Loop (5–10x, bar unchanged)  │
   └───────────────────────────┬────────────────────────────┘
                               ▲                           │
                               └───── Iterate 2 → 5 ───────┘
```

### 4.1 Stage 1: Dataset & Conversation Scenario Preparation
Prepare a deterministic dataset before testing:
1. **Deterministic Test Cases**: `(Prompt, Response, Reference, Invariants)` tuples.
2. **Multi-Turn Conversation Simulation**: For conversational or tool-calling agents, test the full conversation trace (`AgentTrace` $\to$ `ConversationTurn` $\to$ `AgentEvent`), not isolated prompt fragments.
3. **Synthetic User Persona Scenarios**: When real data is insufficient (cold-start), generate synthetic conversation scenarios with explicit simulation instructions (role, constraints, goals) and a turn limit (`max_turns: 3–10`).

### 4.2 Stage 2: Inference Run & Simulation
- **Model Evaluation**: Test output determinism at `temperature: 0` or with a fixed seed.
- **Multi-Turn Agent Evaluation**: Run the agent callable against a user simulator that plays the scenario until it completes or reaches the `max_turns` limit.

### 4.3 Stage 3: Strict Grading (Grading & Grounding)
- **Deterministic Local Metrics**: Evaluate JSON schema, static-pattern regex, latency and token tolerances, and business invariant checks in-process.
- **LLM-as-a-Judge**: Use a frontier judge model with a strict binary rubric ($0$ or $1$), and require it to extract a text evidence quote before the final verdict.

### 4.4 Stage 4: Loss Clustering & Root-Cause Taxonomy
Do not repair failures one at a time in random order. Assign every failed test case to one of 5 main failure classes:

| Failure Class | Observed Symptom | Remediation |
|---|---|---|
| **Instruction Drift** | The model ignores role constraints or produces a format outside the contract | Tighten the static part of the system prompt, lock the rule order |
| **Lost-in-the-Middle Context Miss** | Critical information is ignored because it sits in the middle of a long chunk | Reorder the context: put critical facts at the start or directly before the question |
| **Tool / Schema Mismatch** | Function call parameters violate a data type or enum | Tighten the JSON schema (`strict: true`), add a minimal example to the tool description |
| **Ungrounded Hallucination** | The model claims a fact that is not written in the context references | Add an explicit refusal instruction: when evidence is absent, state that it was not found |
| **Boundary / Edge Case Break** | Empty input, special characters, or context overflow | Add input sanitization and controlled truncation in the application layer |

### 4.5 Stage 5: Iterative Remediation Loop & No Shortcuts

Run 5–10 repair iterations on the prompt and agent instructions until the quality target is met.

**Shortcuts That Damage Quality (Strictly Prohibited):**

| Shortcut | Why It Is Rejected | Correct Action |
|---|---|---|
| *"I lowered the score threshold so it passes."* | It hides a real defect. | Fix the prompt or agent instructions; do not lower the quality bar. |
| *"This case is flaky and sometimes fails, so skip it."* | Flakiness signals non-determinism. | Use `temperature: 0` or more deterministic instructions. |
| *"I adjusted the dataset's expected output to match the agent's answer."* | The test dataset represents domain truth. | Fix the agent's behaviour so its output matches the domain. |
| *"One sample trace looks good, so skip the full test run."* | Evaluating one sample does not guarantee generalization. | Run the whole regression test suite (at least 30 samples). |
| *"One repair iteration is enough."* | Changing one prompt often triggers a regression in another metric. | Re-run the whole test suite every time the prompt changes. |
