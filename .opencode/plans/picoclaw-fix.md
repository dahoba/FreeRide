# PicoClaw V2 Protocol Error Fix Plan

**Goal:** Fix the `unknown protocol "google"` error and remove the redundant `openrouter/` prefix from `model_name` aliases.

**The Cause:** 
1. `ensure_model_in_list` was updating existing `model_list` entries but skipping injecting the `provider: "openrouter"` field. When `provider` is missing, PicoClaw falls back to parsing the `model` string (`google/...`), which extracts an unknown protocol (`"google"`).
2. The `model_name` aliases were still keeping the `openrouter/` prefix, which was confusing and unnecessary under the new V2 schema.

### Task 1: Update main.py
1. **Modify `format_model_for_picoclaw` default argument:**
   Change `with_provider_prefix: bool = True` to `with_provider_prefix: bool = False`. This ensures all aliases generated are clean (e.g. `google/lyria-3-pro-preview:free`).
   ```python
   def format_model_for_picoclaw(
       model_id: str, with_provider_prefix: bool = False, append_free: bool = True
   ) -> str:
   ```

2. **Update `ensure_model_in_list` to enforce `provider` and `model` on existing entries:**
   When iterating over existing entries, forcefully set `provider` to `"openrouter"` and `model` to `native_model` so PicoClaw explicitly routes the model correctly:
   ```python
       for entry in config["model_list"]:
           if entry.get("model_name") == formatted_name:
               entry["api_keys"] = api_keys
               entry["provider"] = "openrouter"
               entry["model"] = native_model
               if fallbacks is not None:
                   entry["fallbacks"] = fallbacks
               return
   ```
   Also change `formatted_name` to use `with_provider_prefix=False`:
   ```python
   formatted_name = format_model_for_picoclaw(model_id, with_provider_prefix=False)
   ```

3. **Update `update_model_config` and `cmd_fallbacks` formatting calls:**
   Make sure all calls explicitly use `with_provider_prefix=False` for the primary model name and fallbacks if they still explicitly pass `True` (or rely on the new default).

### Task 2: Update watcher.py
1. **In `rotate_to_next_model`:**
   Change the `formatted_primary` assignment to use `with_provider_prefix=False`.
   Change the `fb` assignment for fallbacks to use `with_provider_prefix=False`.

**Verification:**
After executing these edits, running `freeride auto` should generate a `config.json` where `agents.defaults.model_name` is exactly equal to the `model_name` field in `model_list` (without `openrouter/`), and every object in `model_list` explicitly has `"provider": "openrouter"`.