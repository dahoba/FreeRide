# FreeRide Agent Instructions

This file contains crucial context for AI agents working on the FreeRide repository.

## Project Architecture & Setup
- **Type**: Python-based PicoClaw skill plugin.
- **Entrypoints**: `main.py` (provides the `freeride` CLI) and `watcher.py` (provides the `freeride-watcher` daemon).
- **Setup**: Run `uv pip install -e .` (or `pip install -e .`) to install the package and its CLI commands locally.
- **Dependencies**: Minimal (relies on `requests` as per `requirements.txt`).

## Environment & Testing
- **Required Env Var**: `OPENROUTER_API_KEY` must be set for any API calls to OpenRouter. It can be a single key or a JSON array string of multiple keys.
- **Manual Testing**: There is no automated test suite. Test changes by running `freeride status`, `freeride list`, or `freeride auto`. 
- **Integration Testing**: To test with PicoClaw, you must have PicoClaw installed.

## Crucial Quirks & Workflows
- **Configuration Target**: The skill writes to `~/.picoclaw/config.json`, specifically modifying `agents.defaults.model` and `agents.defaults.models`.
- **Restart Requirement**: After any code changes that affect configuration written to `config.json` (or manual test executions like `freeride auto`), you **MUST** run `picoclaw gateway restart` for PicoClaw to pick up the changes.
- **State Files**: Watcher state and caches are stored in `~/.picoclaw/.freeride-watcher-state.json` and `~/.picoclaw/.freeride-cache.json`.