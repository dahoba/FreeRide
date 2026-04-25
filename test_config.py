import json
import os
os.environ["PICOCLAW_CONFIG"] = "./test_config.json"
from main import update_model_config, load_picoclaw_config
import main

# Mock get_api_keys
main.get_api_keys = lambda: ["sk-or-v1-123"]
main.get_api_key = lambda: "sk-or-v1-123"
main.get_free_models = lambda api_key: [{"id": "google/lyria-3-pro-preview:free", "context_length": 1000, "_score": 0.9}]

update_model_config("google/lyria-3-pro-preview:free", as_primary=True, add_fallbacks=True)

with open("./test_config.json", "r") as f:
    print(json.dumps(json.load(f), indent=2))
