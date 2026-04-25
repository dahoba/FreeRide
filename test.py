import json

def test():
    config = {"model_list": [{"model_name": "openrouter/google/lyria", "model": "google/lyria"}]}
    
    # ensure_model_in_list
    for entry in config["model_list"]:
        if entry.get("model_name") == "openrouter/google/lyria":
            entry["provider"] = "openrouter"
            entry["model"] = "google/lyria"
            return config

print(json.dumps(test(), indent=2))
