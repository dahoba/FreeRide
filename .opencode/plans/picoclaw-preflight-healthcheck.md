# Plan: Add Pre-flight Health Check to `freeride auto`

**Goal:** Before setting a model as primary, `freeride auto` should test if it's actually available (not rate limited). This prevents configuring a broken setup.

**Architecture:**
1. Move the `OPENROUTER_CHAT_URL` constant and `test_model()` function from `watcher.py` to `main.py`
2. Update `watcher.py` to import `test_model` from `main.py`
3. Modify `cmd_auto()` to test the top N models before selecting one

---

### Task 1: Move health check utilities to `main.py`

Add to `main.py` (near the other constants around line 27):
```python
OPENROUTER_CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"
```

Add the `test_model()` function (moved from `watcher.py`):
```python
def test_model(api_key: str, model_id: str) -> tuple[bool, Optional[str]]:
    """Test if a model is available by making a minimal API call."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/Shaivpidadi/FreeRide",
        "X-Title": "FreeRide Health Check",
    }
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": "Hi"}],
        "max_tokens": 5,
        "stream": False,
    }
    try:
        response = requests.post(
            OPENROUTER_CHAT_URL, headers=headers, json=payload, timeout=30
        )
        if response.status_code == 200:
            return True, None
        elif response.status_code == 401:
            return False, "invalid_key"
        elif response.status_code == 429:
            return False, "rate_limit"
        elif response.status_code == 503:
            return False, "unavailable"
        else:
            try:
                body = response.json()
                err_code = body.get("error", {}).get("code", "")
                err_msg = str(body.get("error", {}).get("message", ""))
                if err_code == "model_not_found" or "Unknown model" in err_msg:
                    return False, "model_not_found"
            except Exception:
                pass
            return False, f"error_{response.status_code}"
    except requests.Timeout:
        return False, "timeout"
    except requests.RequestException as e:
        return False, "request_error"
```

### Task 2: Update `watcher.py` to import from `main.py`

Remove `OPENROUTER_CHAT_URL` and `test_model` from `watcher.py`.

Update imports in `watcher.py`:
```python
from main import (
    get_api_keys,
    get_free_models,
    load_picoclaw_config,
    save_picoclaw_config,
    ensure_config_structure,
    format_model_for_picoclaw,
    ensure_model_in_list,
    get_picoclaw_config_path,
    test_model,  # NEW
)
```

### Task 3: Modify `cmd_auto()` in `main.py`

Replace the model selection logic:
```python
def cmd_auto(args):
    """Automatically select the best free model."""
    api_key = get_api_key()
    if not api_key:
        print("Error: OPENROUTER_API_KEY not set")
        sys.exit(1)

    config = load_picoclaw_config()
    current_primary = get_current_model(config)

    print("Finding best free model...")
    models = get_free_models(api_key, force_refresh=True)

    if not models:
        print("Error: No free models available.")
        sys.exit(1)

    # Test top models and pick the first available one
    best_model = None
    tested = 0
    max_tests = 5  # Don't test more than 5 models (to avoid excessive API calls)

    for m in models:
        if "openrouter/free" in m["id"]:
            continue
        if tested >= max_tests:
            break

        model_id = m["id"]
        print(f"  Testing {model_id}...", end=" ")
        success, error = test_model(api_key, model_id)
        tested += 1

        if success:
            print("OK")
            best_model = m
            break
        elif error == "rate_limit":
            print("rate limited, skipping")
        elif error == "model_not_found":
            print("not found, skipping")
        else:
            print(f"{error}, skipping")

    if not best_model:
        print("All top models unavailable, using openrouter/free as fallback")
        # Use openrouter/free as primary since all tested models failed
        best_model = {"id": "openrouter/free", "context_length": 0, "_score": 0}

    model_id = best_model["id"]
    context = best_model.get("context_length", 0)
    score = best_model.get("_score", 0)

    # ... rest of the function remains the same
```

### Task 4: Verify and commit

1. Run `python3 main.py --help` and `python3 watcher.py --help` to verify syntax
2. Commit with message: `feat: Add pre-flight health check to freeride auto`

---

**Key decisions:**
- `max_tests = 5` — balances speed (each test takes ~1-2 seconds) vs finding an available model
- Falls back to `openrouter/free` if all tested models fail
- Preserves existing fallback configuration