---
name: ship-critic
version: "1.0.0"
description: "Rubric-driven PASS/REVISE gate evaluator for Ship Engine. Scores every deliverable before gates advance."
argument-hint: '--ticket <ID> --stage <stage> | --gate <gate> | --cross-check --run-id <ID>'
allowed-tools: Bash, Read
homepage: https://github.com/maxtechera/ship
repository: https://github.com/maxtechera/ship
author: maxtechera
license: MIT
user-invocable: false
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      env: []
      optionalEnv: []
      bins: []
    tags:
      - critic
      - quality-gate
      - ship-engine
      - rubric
      - evaluation
---

# Ship Critic — Self-Sufficient Evaluator

Deterministic evaluation contract for Ship Engine. A supervisor (or evaluator agent) runs this
logic by following this document and the rubric files — no Python required.

**Decision lock**: critic runs before every gate and before any deliverable can move to `verified`.
`REVISE` blocks advancement unless a valid override is present.

---

## Invocation Contract

| Argument | Description |
|----------|-------------|
| `--ticket <ID>` | Linear ticket identifier to evaluate |
| `--stage <stage>` | Stage name for rubric lookup in deliverable mode (`validate`, `strategy`, `awareness`, `lead-capture`, `nurture`, `closing`, `launch`, `measure`) |
| `--deliverable <type>` | Artifact key being checked (`validation_report`, `icp`, `ship_plan`, etc.) |
| `--run-id <ID>` | Parent run ticket identifier (required for cross-check) |
| `--gate <gate>` | Gate mode selector (`gate-v`, `gate-s`, `gate-l`) |
| `--cross-check` | Run full cross-deliverable consistency review for the run |
| `--list-rubrics` | List available rubric names from `supervisors/critic/rubrics/*.md` |

### Mode selection

- `--list-rubrics` only: print rubric names and stop
- `--cross-check` requires `--run-id`
- `--gate` mode requires `--ticket`
- Deliverable mode requires `--ticket`, `--stage`, and `--deliverable`
- Invalid combination → return usage error

---

## Rubric Loading Rules

Rubric directory: `supervisors/critic/rubrics/`

- Deliverable mode loads `rubrics/{stage}.md`
- Gate mode loads `rubrics/{gate}.md` (e.g., `gate-v`, `gate-s`, `gate-l`)
- Cross-check mode loads `rubrics/cross-check.md`

**Missing rubric fallbacks:**
- Deliverable mode: `No specific rubric found. Check that the artifact is linked, non-empty, and uses VoC language.`
- Gate mode: `Verify: (1) all hard-gate required fields present, (2) evidence links resolve, (3) kanban proof blocks complete, (4) all deliverables in this stage have critic PASS.`
- Cross-check mode: emit warning, skip with non-blocking exit.

---

## Required Inputs

- Primary evaluated content: Linear issue JSON for `--ticket` (or `--run-id` in cross-check mode)
- Run context: Linear issue JSON for `--run-id` when different from `--ticket`
- Optional linked artifact content: include enough excerpts to score every rubric check without fabrication

Content trimming:
- Primary ticket payload: first ~4000 chars
- Run context payload: first ~2000 chars

If content is unavailable, do not guess. Mark the affected check as `REVISE` with note `content not provided - cannot evaluate`.

---

## Evaluation Procedure (Deterministic)

### 1) Load rubric

Parse every numbered check row in the rubric table. Preserve numbering and check names exactly.

### 2) Score every check

For each check:
- `PASS`: PASS criteria satisfied by provided evidence
- `REVISE`: REVISE trigger is hit, evidence is missing, or content cannot be evaluated safely
- `WARN` (optional): partial degradation that does not independently block; include in notes

No check may be omitted. Every numbered rubric check must appear in the output table.

### 2.1) Numeric scoring thresholds (preserved exactly)

When a rubric check references numeric thresholds, apply them as written:

- `validate` check 5: `behavioral_evidence_ratio >= 50%`, or confidence must be capped at `0.79`
- `validate` check 7: dimension score `>= 4.0` requires `>= 3` strong sources per dimension
- `validate` check 8 and `gate-v` check 8 recommendation thresholds:
  - `>= 4.0` → ship
  - `3.0-3.9` → explore
  - `< 3.0` → kill

Never reinterpret these thresholds. If evidence is insufficient, mark `REVISE`.

### 3) Cross-check logic

In explicit cross-check mode, evaluate all checks in `rubrics/cross-check.md`.
For gate checks, include cross-deliverable consistency findings when applicable to the gate packet.

### 4) Aggregate verdict

- `PASS` only when all required checks are `PASS` and no critical consistency failures exist
- `REVISE` when any check is `REVISE`, any required artifact is missing, or any critical consistency drift is present
- Conservative default: if verdict cannot be confidently extracted, treat as `REVISE`

---

## Output Format (Exact)

Return only this markdown structure (no preamble, no sign-off):

```markdown
### Critic Review - {DELIVERABLE_OR_GATE} - {PASS/REVISE}

**Verdict:** PASS / REVISE

**Checked at:** {ISO-8601 UTC}

#### Checks
| # | Check | Result | Note |
|---|-------|--------|------|
| 1 | ... | PASS / REVISE | ... |

#### Fix List (omit section if PASS)
1. **[Check #N]** Specific fix instruction

#### Cross-Deliverable Consistency (omit section if not cross-check mode)
| Check | Result | Note |
|-------|--------|------|

#### Override (Max only — include only if REVISE)
To override, add a comment on this ticket:
decision: approve
override_reason: <why>
```

---

## Verdict Extraction

When supervisors parse critic output:
1. Inspect the `Verdict:` line
2. If not found, scan full output for `REVISE` then `PASS`
3. If ambiguous or missing, default to `REVISE`

Exit parity:
- `PASS` → exit code equivalent `0`
- `REVISE` (or error) → exit code equivalent `1`
- If evaluator tooling is unavailable: return conservative `REVISE` with concrete fix instruction

---

## Linear Writeback Contract

After each run:
- Post critic markdown to the evaluated Linear ticket
- Write blackboard key `{stage}.{artifact}.critic_verdict` for deliverable checks
- Write blackboard key `{gate}.gate_packet.critic_verdict` for gate checks
- Write blackboard key `cross.consistency.critic_verdict` for cross-check

Structured value: `{key} = PASS|REVISE` + timestamped trace note.

---

## Rubric Catalog

| Rubric | File |
|--------|------|
| Intake | `rubrics/intake.md` |
| Validate | `rubrics/validate.md` |
| Strategy | `rubrics/strategy.md` |
| Awareness | `rubrics/awareness.md` |
| Lead Capture | `rubrics/lead-capture.md` |
| Nurture | `rubrics/nurture.md` |
| Closing | `rubrics/closing.md` |
| Launch | `rubrics/launch.md` |
| Measure | `rubrics/measure.md` |
| Gate-V | `rubrics/gate-v.md` |
| Gate-S | `rubrics/gate-s.md` |
| Gate-L | `rubrics/gate-l.md` |
| Cross-Check | `rubrics/cross-check.md` |

---

## Supervisor Integration

- Invoke critic before each hard gate and before any deliverable transitions to `verified`
- Do not advance while verdict is `REVISE` unless override is explicitly recorded
- Override text contract: `decision: approve` + `override_reason: <why>`

## Done Criteria per Invocation

- Rubric loaded and all checks scored
- PASS/REVISE verdict emitted using required format
- Linear comment posted
- Blackboard verdict key written
- If `REVISE`, fix list is concrete and check-numbered
