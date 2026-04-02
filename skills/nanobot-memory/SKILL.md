# nanobot-memory

## Purpose

Use this skill when the user asks to:
- add persistent memory to nanobot
- inspect or maintain the local memory database
- verify memory recall injection
- split the memory enhancement into a standalone reusable project
- re-apply memory patch after nanobot upgrade

## What this skill provides

- local SQLite-backed persistent message memory
- recall injection via `<relevant-memories>` blocks
- runtime metadata stripping
- duplicate suppression support
- extracted standalone project layout under `nanobot-memory-kit/`

## Project paths

- project root: `/root/.nanobot/workspace/nanobot-memory-kit`
- module: `/root/.nanobot/workspace/nanobot-memory-kit/src/nanobot_memory`
- patch docs/scripts: `/root/.nanobot/workspace/nanobot-memory-kit/patches`

## Safe workflow

1. Back up current nanobot `loop.py`
2. Compare current installed `loop.py`
3. Apply patch via `scripts/apply_patch.sh`
4. Verify via `scripts/verify_gateway.sh`

## Notes

- This is a local-memory enhancement project for nanobot, not an OpenClaw JS plugin.
- Storage is local SQLite only unless the operator changes code.
