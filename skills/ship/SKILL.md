---
name: ship
version: "0.3.0"
description: "GTM pipeline with team mode. /ship spawns coordinator + executor + critic team, renders a live dashboard, and routes active runs by stage."
argument-hint: 'ship (dashboard + team), ship create "<idea>", ship status [RUN-ID], ship run <RUN-ID>'
allowed-tools: Bash, Read, Write
homepage: https://github.com/maxtechera/ship
repository: https://github.com/maxtechera/ship
author: maxtechera
license: MIT
user-invocable: true
triggers:
  - ship
  - ship create
  - ship status
  - ship run
---

# ship

Run `/ship` once. A coordinator team spawns, the dashboard renders, and work starts moving.

Use this skill when the user wants to create, resume, or inspect a GTM run.

## Commands

| Command | Description |
|---------|-------------|
| `/ship` | Spawn the coordinator team and render the live dashboard |
| `/ship create "<idea>"` | Create a new run ticket, preflight credentials, and hand off to the engine |
| `/ship status [RUN-ID]` | Read the active run, stage, last update, and blockers |
| `/ship run <RUN-ID>` | Resume an existing run |

## Required references

Before acting, read these repo files as needed:

- `SKILL.md`
- `engine/WORKFLOW.md`
- `credentials/registry/core.yml`
- `supervisors/engine/SKILL.md`
- `content/engine/SKILL.md`

## Notes

- Run credential preflight before deploy actions.
- Use orchestrator-style verification before advancing stages.
- Keep the dashboard and run state aligned with the active Linear ticket.
