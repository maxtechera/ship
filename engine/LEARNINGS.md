# Ship Engine — Learnings

Institutional memory. Every completed or killed run adds an entry. This file feeds forward into future runs.

---

_No runs completed yet. First entry will be added when a ship run reaches Done or Killed._

---

## Pre-Run Review: Architecture Audit ([REDACTED_PHONE])

Before the first real run, a full review of the spec, templates, intake script, and archive surfaced these operational realities. Capturing now so Run 1 doesn't learn them the hard way.

### SKILL.md Size Problem
- SKILL.md is ~930 lines. A sub-agent spawned for a single stage (e.g., Outbound) receives the entire pipeline spec as context — burning tokens on 11 stages it doesn't need.
- **Recommendation:** Decompose into per-stage docs (`stages/validate.md`, `stages/outbound.md`, etc.) that sub-agents load only when working that stage. SKILL.md becomes the orchestrator-level overview + stage index.

### Tool Gap Reality
8 tools referenced throughout the spec don't exist yet:
| Tool | Used In | Fallback Available? |
|------|---------|-------------------|
| `mailerlite.py` | Lead Capture, Nurture, Closing | MailerLite API via `web_fetch` / manual |
| `reddit.py` | Validate, Outbound | `web_search "reddit {query}"` + `web_fetch` |
| `cold-email.py` | Outbound | `gog` Gmail directly |
| `stripe.py` | Closing | Stripe Dashboard manual / API via `web_fetch` |
| `utm.py` | Lead Capture, Measure | Manual UTM builder or inline generation |
| `x-outreach.py` | Outbound | `research.py --x-only` for discovery, manual for engagement |
| `testimonials.py` | Closing, Marketing | Manual collection |
| `landing-gen.py` | Lead Capture | `coding-agent` / `create-app` skill |

**Key insight:** The spec's "Tool Resilience" section already says "if tool doesn't exist, use manual equivalent" — but stage sub-agents need explicit fallback instructions per tool, not just the philosophy. When a stage agent hits `reddit.py` and it doesn't exist, it should know *exactly* what to do instead.

### Channel Routing Mismatch
- Spec claims "channel-agnostic" but has Telegram group IDs and inline button patterns baked into multiple sections.
- The engine should use OpenClaw's `message` tool with channel routing — let the platform handle where messages go.
- **Concrete issue:** `neo-ship-engine` Telegram group (-[REDACTED_PHONE]) is referenced as the primary notification surface. On instances without Telegram (e.g., Slack-only), this silently fails.
- **Fix:** Notification targets should be configurable per-run or per-instance, not hardcoded in the spec.

### Intake Script Is a One-Off (Now a Skill)
- The intake tool has been converted to the `ship-engine-intake` skill (`skills/ship-engine-intake/SKILL.md`). It creates Linear tickets for 3 hardcoded offers (Command Center, CRM, AI Business OS Setup). It's not a general-purpose intake tool.
- The legacy `engine.py` CLI is deprecated. Ship Engine is skills-first and runs via `ship-engine-supervisor` + stage supervisors.
- **Implication:** Run 1 will need manual Linear setup or a generalized intake flow. The spec describes commands that can't be executed.

### External State Dependencies
- Drive folder structure per run (`Ship Engine / {name} /` with 11 subdirectories) assumes Google Drive integration is wired up. It's available via `gog` but folder creation automation doesn't exist.
- Figma project per run assumes Figma API access — not configured anywhere.
- **Pragmatic alternative:** Use the workspace filesystem (`skills/engine/runs/{ticket-id}/`) as primary artifact storage. Drive/Figma as optional enhancements when available.

### Validation Framework Is Standalone-Valuable
- The 5-level validation process (Pain Discovery → Demand Quantification → Willingness to Pay → Audience-Market Fit → Score Card) is the most immediately useful piece of the entire engine.
- It works without any of the missing tools — just `web_search`, `web_fetch`, `research.py`, and LLM reasoning.
- Could be extracted as a standalone skill (`validate-idea`) usable outside the ship engine context.

### Quality Gates as Reusable Pattern
- The critic-agent pattern (lightweight sub-agent + rubric → PASS/REVISE/FAIL) is applicable beyond ship engine:
  - Content quality checks before publishing
  - Code review automation
  - Research report verification
- Worth extracting into a shared pattern doc (`docs/QUALITY_GATE_PATTERN.md`) once proven in ship engine runs.

### Parallel Sub-Agent Execution
- The 6-stage concurrent execution model maps directly to `sessions_spawn` — this is already proven in the workspace (NEO-135 ran 4 parallel sub-agents successfully).
- Key constraint learned from NEO-135: sub-agents hit 200K token limits on complex tasks. Ship engine stages need lean, focused prompts — another argument for per-stage docs instead of the full SKILL.md.

### Archive Is Empty
- `archive/MAX-244/` directory exists but contains no files. Whatever happened with MAX-244, no artifacts survived.
- LEARNINGS.md had zero entries before this audit.
- **The engine has never completed a full run.** Run 1 is a true first test — expect friction at every stage boundary.

### Template Coverage
- 12 templates exist and total ~1,645 lines. The `ship-checklist.md` alone is 931 lines (350+ items).
- Templates are well-structured but untested against real data.
- The massive checklist may overwhelm sub-agents — consider a "minimum viable checklist" variant for v1 runs.

### Nested Skill Directory
- There's a duplicate `skills/engine/engine/` directory with its own SKILL.md and templates — likely a copy artifact. Should be cleaned up to avoid confusion about which is authoritative.
