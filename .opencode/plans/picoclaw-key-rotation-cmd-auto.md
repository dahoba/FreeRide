# Plan: Add Key Rotation to `cmd_auto` Model Testing

**Goal:** When testing models in `cmd_auto`, try all available API keys if the first one is rate limited, instead of skipping the model.

**Problem:** Currently `cmd_auto` calls `get_api_key()` which returns only the first key. If that key is rate limited, all models appear unavailable even though other keys might work.

**The Fix:**
1. Add a `test_model_all_keys()` function in `main.py` that tries all keys without persistent state tracking
2. Update `cmd_auto` to use `test_model_all_keys()` instead of `test_model()`

### Task 1: Add `test_model_all_keys()` to `main.py`

```python
def test_model_all_keys(model_id: str) -> tuple[bool, Optional[str], Optional[str]]:
    """Test if a model is available, trying all API keys on 429.
    Returns (success, error, working_key).
    """
    keys = get_api_keys()
    if not keys:
        return False, "no_keys", None

    for key in keys:
        success, error = test_model(key, model_id)
        if success:
            return True, None, key
        if error != "rate_limit":
            return False, error, key  # non-key error (not_found, unavailable, etc)
        # 429: try next key

    return False, "rate_limit", None  # all keys exhausted with 429
```

### Task 2: Update `cmd_auto()` in `main.py`

Replace:
```python
success, error = test_model(api_key, model_id)
```

With:
```python
success, error, working_key = test_model_all_keys(model_id)
```

---

**Note:** No state tracking needed — `cmd_auto` is a one-time operation. The watcher handles persistent key state separately.