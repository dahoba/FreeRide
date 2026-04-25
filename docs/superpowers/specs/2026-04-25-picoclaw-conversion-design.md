# FreeRide -> PicoClaw Conversion Specification

## Purpose
Convert the FreeRide skill from targeting OpenClaw to targeting PicoClaw. The goal is to update all paths, references, and documentation to align with PicoClaw's architecture while retaining the original `freeride` CLI name and functionality.

## Core Design

### 1. Environment-Aware Path Resolution
FreeRide will stop using hardcoded paths and instead use PicoClaw's standard environment variables for configuration and data storage.

*   **Config File**: 
    *   Primary: `os.environ.get("PICOCLAW_CONFIG")`
    *   Fallback: `~/.picoclaw/config.json`
*   **Data Directory**:
    *   Primary: `os.environ.get("PICOCLAW_HOME")`
    *   Fallback: `~/.picoclaw`
*   **State & Cache Files**:
    *   Cache: `{PICOCLAW_HOME}/.freeride-cache.json`
    *   State: `{PICOCLAW_HOME}/.freeride-watcher-state.json`

### 2. Config Schema Compatibility
Based on the PicoClaw docs, the model configuration schema (`agents.defaults.model` and `agents.defaults.models`) remains identical to OpenClaw. The logic for reading and writing to this JSON structure will remain unchanged, only the file path will change.

### 3. File Updates

#### `main.py`
*   Replace hardcoded `OPENCLAW_CONFIG_PATH` with a dynamic function `get_picoclaw_config_path()`.
*   Replace hardcoded `CACHE_FILE` with a dynamic function `get_cache_file_path()`.
*   Rename internal functions referencing "openclaw" (e.g., `load_openclaw_config` -> `load_picoclaw_config`, `save_openclaw_config` -> `save_picoclaw_config`).
*   Update CLI output messages replacing "OpenClaw" with "PicoClaw".

#### `watcher.py`
*   Replace hardcoded `STATE_FILE` with a dynamic function `get_state_file_path()`.
*   Update imported function names from `main.py` to match the new PicoClaw names.

#### `skill.json`
*   Change the root key `"openclaw"` to `"picoclaw"`.
*   Update `"configPath"` to `~/.picoclaw/config.json`.
*   Update `"install"` script path from `~/.openclaw/workspace/...` to `~/.picoclaw/workspace/...`.
*   Update description strings.

#### Documentation (`README.md`, `SKILL.md`, `AGENTS.md`)
*   Replace all instances of `OpenClaw` with `PicoClaw`.
*   Replace all instances of `openclaw gateway restart` with `picoclaw gateway restart`.
*   Replace all instances of `~/.openclaw/openclaw.json` with `~/.picoclaw/config.json`.
*   Replace all instances of `~/.openclaw/workspace/...` with `~/.picoclaw/workspace/...`.
*   Replace all instances of `openclaw config set ...` with `picoclaw config set ...`.
*   Replace all instances of `openclaw doctor --fix` with `picoclaw doctor --fix`.
*   Replace all instances of `openclaw models list` with `picoclaw models list`.
*   Replace all instances of `openclaw dashboard` with `picoclaw dashboard`.

## Out of Scope
*   Renaming the `freeride` or `freeride-watcher` commands themselves.
*   Adding new features or changing the OpenRouter rating logic.
*   Supporting both OpenClaw and PicoClaw simultaneously (the project is migrating entirely to PicoClaw).