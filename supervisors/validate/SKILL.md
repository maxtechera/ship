---
name: ship-validate-supervisor
description: Own Stages 2-3 (Validate + Post-Validation gate). Produces Validation Report + ICP with evidence, enforces scoring, and routes Max decision.
---

# Ship Validate Supervisor

Own Stage 2 (VALIDATE) and Stage 3 (Post-Validation approval gate). The output is an intelligence package that downstream stages reuse verbatim.

## Shared Contracts (DRY)
Follow canonical contracts in `openclaw-config/skills/ship-engine/WORKFLOW.md`:
- `Gate Prefill Requirement (Max-Facing)`
- `Writeback Schema (Canonical)`
- `Deliverable Lifecycle States (Stage 9)`

## Inputs (Required)
- `intake.product_brief` (linked doc)
- `intake.research_kickoff` (linked doc)
- Access to research tools/sources
- Linear Stage 2 + Stage 3 tickets

## ICP Discovery (Mandatory First Step)

Before validation research, execute comprehensive ICP discovery:

1. **Read** `skills/icp-discovery/SKILL.md`
2. **Brainstorm** 20-30 potential ICPs (NOT just 3 "obvious" ones)
3. **Score** all ICPs using weighted rubric (Pain 30%, Market 20%, Competition 20%, Channel 15%, Timing 15%)
4. **Rank** and select top 5-10 for validation
5. **Document** in separate ICP discovery file (universe, scoring, selection)

**Anti-pattern:** Starting validation with only 3 ICPs  
**Correct pattern:** Brainstorm 20-30 → Score all → Validate top 5-10

**Why:** Premature narrowing kills high-potential segments. The AlphaAgent session started with 3 developer ICPs, expanded to 25 after Max's feedback, and the top 2 final picks weren't in the original 3.

**Deliverable files:**
- `icp-universe.md` — All 20-30 segments across dimensions (user type, company size, use case, pain, vertical)
- `icp-scoring.md` — Scoring matrix with rationale per ICP
- `top-5-selection.md` — Selected ICPs with rationale + contrarian picks

## Deliverables (Required)
- [ ] Comprehensive ICP discovery (20+ segments brainstormed, all scored, top 5-10 selected)
- [ ] Validation report (evidence + scoring + recommendation) linked in Linear
- [ ] ICP document (VoC bank + channel map) linked in Linear
- [ ] Max decision request posted as a prefilled Decision Packet (Ship / Explore / Kill)
- [ ] Blackboard keys written using `{stage}.{artifact}`

## Quality Gate (PASS/REVISE)
PASS requires:
- Evidence: direct quotes + source URLs + recency signal
- Clear ICP segmentation (not "developers")
- Competitive landscape summary with gaps
- Weighted scoring applied with written justification
- Recommendation includes explicit risks + de-risking steps

REVISE triggers:
- any major claim without a source URL
- ICP too broad to be actionable
- scoring missing or inconsistent

## Verification
- Every major claim has a source URL
- PRIMARY sources (Reddit, HN, X) > secondary sources (analyst reports)
- VoC bank includes exact phrases (copy-ready)
- Scoring rubric filled and arithmetic checked
- In `production`, Validation outputs are critic-verified (`PASS`) before marking `verified`

## Writeback Contract
- Blackboard keys:
  - `validate.validation_report`
  - `validate.icp`
  - `validate.research_dataset`
  - `validate.research_brief`
  - `validate.score`
  - `validate.recommendation`
  - Include `status_summary`, `next_steps`, and `critic_verdict` in `production`
- Linear:
  - Stage 2 ticket Deliverables checklist reflects real artifacts
  - Stage 2 comments include `status_summary` + `next_steps` on meaningful updates
  - Stage 3 ticket contains prefilled Decision Packet (canonical template) + links

## Delegation Map
- Research synthesis + vaulting: `research`
- Writing/humanization: `content-copy`

## Failure Policy
- If sources are thin: downgrade confidence explicitly and switch to deeper competitive research + alternative channels
- If costs/quotas block research: use cheaper sources first; note gaps; do not fabricate

## Critic Invocation (Required in `production`)
Before posting the Gate-V Decision Packet:
1. Assemble context bundle: `intake.product_brief` (summary) + `validate.validation_report` + `validate.icp` (VoC phrases)
2. Spawn `ship-critic` with `check_type=gate`, `gate=gate-v`
3. Wait for verdict:
   - **PASS** → post Decision Packet immediately
   - **REVISE** → post revision requests to Stage 2 ticket; do NOT post Decision Packet; fix issues and re-run critic
4. Record `critic.gate-v` in blackboard with `verdict`, `verdict_summary`, `comment_url`, `checked_at`
5. On Max override (`override: approve` in a comment): record override in blackboard; post Decision Packet

## Done When
- Stage 2 deliverables exist + verification recorded
- Critic has returned PASS (or Max override is recorded) for Gate-V
- Stage 3 gate message is posted as a prefilled Decision Packet with links and a clear decision request
