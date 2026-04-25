# PicoClaw Conversion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the FreeRide skill to use PicoClaw's configuration and workspace paths instead of OpenClaw's.

**Architecture:** We will replace hardcoded `~/.openclaw` paths with dynamic resolution using `os.environ.get("PICOCLAW_CONFIG")` and `os.environ.get("PICOCLAW_HOME")`, falling back to `~/.picoclaw`. We will also rename all `openclaw` references in code and docs to `picoclaw`.

**Tech Stack:** Python, JSON

---

### Task 1: Update main.py

**Files:**
- Modify: `main.py`

- [ ] **Step 1: Replace hardcoded paths with dynamic functions**

Add the following path resolution functions at the top of `main.py` (around line 25), replacing the existing `OPENCLAW_CONFIG_PATH` and `CACHE_FILE` constants:

```python
import os
from pathlib import Path

def get_picoclaw_config_path() -> Path:
    env_config = os.environ.get("PICOCLAW_CONFIG")
    if env_config:
        return Path(env_config)
    return Path.home() / ".picoclaw" / "config.json"

def get_cache_file_path() -> Path:
    env_home = os.environ.get("PICOCLAW_HOME")
    if env_home:
        base_dir = Path(env_home)
    else:
        base_dir = Path.home() / ".picoclaw"
    return base_dir / ".freeride-cache.json"
```

- [ ] **Step 2: Rename config functions**

Rename `load_openclaw_config` to `load_picoclaw_config` and update its body to use `get_picoclaw_config_path()`.

```python
def load_picoclaw_config() -> dict:
    config_path = get_picoclaw_config_path()
    if not config_path.exists():
        return {}
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}
```

Rename `save_openclaw_config` to `save_picoclaw_config` and update its body.

```python
def save_picoclaw_config(config: dict):
    config_path = get_picoclaw_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
```

- [ ] **Step 3: Update `format_model_for_openclaw` name**

Rename `format_model_for_openclaw` to `format_model_for_picoclaw`.

- [ ] **Step 4: Update all function calls in main.py**

Replace all instances of:
*   `load_openclaw_config()` with `load_picoclaw_config()`
*   `save_openclaw_config(config)` with `save_picoclaw_config(config)`
*   `format_model_for_openclaw(...)` with `format_model_for_picoclaw(...)`
*   `CACHE_FILE` with `get_cache_file_path()`

- [ ] **Step 5: Update CLI output strings in main.py**

Search and replace the string "OpenClaw" with "PicoClaw" in all `print()` statements and docstrings inside `main.py`. Note: do not change the CLI command names (`freeride`, `freeride-watcher`).

- [ ] **Step 6: Run `main.py` to ensure no syntax errors**

Run: `python main.py --help`
Expected: Outputs the help menu without syntax errors.

- [ ] **Step 7: Commit**

```bash
git add main.py
git commit -m "feat: Update main.py paths and references for PicoClaw"
```

### Task 2: Update watcher.py

**Files:**
- Modify: `watcher.py`

- [ ] **Step 1: Replace hardcoded state path with dynamic function**

Add the path resolution function at the top of `watcher.py` (around line 35), replacing the existing `STATE_FILE` constant:

```python
import os
from pathlib import Path

def get_state_file_path() -> Path:
    env_home = os.environ.get("PICOCLAW_HOME")
    if env_home:
        base_dir = Path(env_home)
    else:
        base_dir = Path.home() / ".picoclaw"
    return base_dir / ".freeride-watcher-state.json"
```

- [ ] **Step 2: Update imports from main.py**

Update the imports from `main` to reflect the new function names:

```python
from main import (
    get_api_keys,
    get_free_models,
    load_picoclaw_config,
    save_picoclaw_config,
    format_model_for_picoclaw,
    get_current_fallbacks
)
```

- [ ] **Step 3: Update all function calls and state file references in watcher.py**

Replace all instances of:
*   `STATE_FILE` with `get_state_file_path()`
*   `load_openclaw_config()` with `load_picoclaw_config()`
*   `save_openclaw_config(config)` with `save_picoclaw_config(config)`
*   `format_model_for_openclaw(...)` with `format_model_for_picoclaw(...)`

- [ ] **Step 4: Update CLI output strings in watcher.py**

Search and replace the string "OpenClaw" with "PicoClaw" in all `print()` statements and docstrings inside `watcher.py`.

- [ ] **Step 5: Run `watcher.py` to ensure no syntax errors**

Run: `python watcher.py --help`
Expected: Outputs the help menu without syntax errors.

- [ ] **Step 6: Commit**

```bash
git add watcher.py
git commit -m "feat: Update watcher.py paths and references for PicoClaw"
```

### Task 3: Update skill.json

**Files:**
- Modify: `skill.json`

- [ ] **Step 1: Update metadata keys and values**

Modify `skill.json` to change the `openclaw` key to `picoclaw` and update the `configPath` and `install` script:

```json
{
  "name": "freeride",
  "displayName": "FreeRide - Free AI for PicoClaw",
  "version": "1.1.0",
  "description": "Unlimited free AI access for PicoClaw via OpenRouter's free models with automatic fallback switching",
  ...
  "picoclaw": {
    "compatible": true,
    "minVersion": "1.0.0",
    "configPath": "~/.picoclaw/config.json",
    "configKeys": [
      "agents.defaults.model",
      "agents.defaults.models"
    ],
    "requiredSecrets": ["OPENROUTER_API_KEY"],
    "networkAccess": ["openrouter.ai"]
  },
  "install": "npx clawhub@latest install free-ride && cd ~/.picoclaw/workspace/skills/free-ride && pip install -e ."
}
```

- [ ] **Step 2: Commit**

```bash
git add skill.json
git commit -m "chore: Update skill.json metadata for PicoClaw"
```

### Task 4: Update Documentation Files

**Files:**
- Modify: `README.md`
- Modify: `SKILL.md`
- Modify: `AGENTS.md`

- [ ] **Step 1: Update `README.md`**

Use `sed` or open the file to perform the following replacements globally:
*   `OpenClaw` -> `PicoClaw`
*   `openclaw gateway restart` -> `picoclaw gateway restart`
*   `openclaw config set` -> `picoclaw config set`
*   `openclaw doctor` -> `picoclaw doctor`
*   `openclaw models list` -> `picoclaw models list`
*   `openclaw dashboard` -> `picoclaw dashboard`
*   `~/.openclaw/openclaw.json` -> `~/.picoclaw/config.json`
*   `~/.openclaw/workspace/` -> `~/.picoclaw/workspace/`
*   `~/.openclaw/` -> `~/.picoclaw/`

- [ ] **Step 2: Update `SKILL.md`**

Perform the same replacements as in `README.md`. Also update the `writes:` section to point to `.picoclaw` files.

- [ ] **Step 3: Update `AGENTS.md`**

Perform the same replacements. Ensure the "Crucial Quirks & Workflows" section mentions `~/.picoclaw/config.json`, `~/.picoclaw/.freeride-watcher-state.json`, and `~/.picoclaw/.freeride-cache.json`, as well as `picoclaw gateway restart`.

- [ ] **Step 4: Commit**

```bash
git add README.md SKILL.md AGENTS.md
git commit -m "docs: Update documentation to reference PicoClaw"
```