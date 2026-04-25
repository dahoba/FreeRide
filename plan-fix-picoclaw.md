# Plan: Fix PicoClaw V2 Protocol Error

**Goal:** Fix the `unknown protocol "google"` error and remove the redundant `openrouter/` prefix from `model_name` aliases.

**The Cause:** 
1. `ensure_model_in_list` was updating existing `model_list` entries but skipping injecting the `provider: "openrouter"` field. When `provider` is missing, PicoClaw falls back to parsing the `model` string (`google/...`), which extracts an unknown protocol (`"google"`).
2. The `model_name` aliases were still keeping the `openrouter/` prefix, which was confusing and unnecessary under the new V2 schema.

### Task 1: Update main.py
1. Modify `format_model_for_picoclaw` to use `with_provider_prefix=False` by default for all `model_name` aliases.
2. In `ensure_model_in_list`, update the code to forcefully set `"provider": "openrouter"` and `"model": native_model` even when modifying an *existing* entry in `model_list`.
3. In `update_model_config` and `cmd_fallbacks`, update the alias variables to use `with_provider_prefix=False`.

### Task 2: Update watcher.py
1. In `rotate_to_next_model`, use `with_provider_prefix=False` for `formatted_primary` and `fallbacks`.
