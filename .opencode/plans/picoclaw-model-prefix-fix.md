# Plan: Fix Model Field to Include openrouter/ Prefix

**Goal:** Fix the `unknown protocol` error by ensuring the `model` field in `model_list` entries always includes the `openrouter/` prefix.

**The Root Cause:**
PicoClaw determines the protocol from the prefix in the `model` field, NOT the `provider` field. When `model` is `"google/lyria-3-pro-preview:free"`, PicoClaw parses `"google"` as the protocol and crashes.

**The Fix (one line):**
In `ensure_model_in_list` (main.py, line ~309), change the `model` field from `native_model` to `format_model_for_picoclaw(model_id, with_provider_prefix=True)`.

**Current code:**
```python
    entry = {
        "model_name": formatted_name,
        "provider": "openrouter",
        "model": native_model,  # BUG: no openrouter/ prefix
        "api_keys": api_keys,
    }
```

**Fixed code:**
```python
    entry = {
        "model_name": formatted_name,
        "provider": "openrouter",
        "model": format_model_for_picoclaw(model_id, with_provider_prefix=True),  # FIXED: always has openrouter/ prefix
        "api_keys": api_keys,
    }
```

**Expected result config:**
```json
{
  "model_name": "google/lyria-3-pro-preview:free",
  "provider": "openrouter",
  "model": "openrouter/google/lyria-3-pro-preview:free",
  "api_keys": ["..."]
}
```