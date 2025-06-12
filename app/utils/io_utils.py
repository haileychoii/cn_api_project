import os
import json

def load_step_results(folder_path):
    results = {}
    for fname in os.listdir(folder_path):
        if fname.endswith(".json"):
            product = fname.replace(".json", "").replace("step2_", "").replace("step4_", "").replace("step5_", "")
            with open(os.path.join(folder_path, fname), "r", encoding="utf-8") as f:
                try:
                    results[product] = json.load(f)
                except Exception as e:
                    results[product] = {"error": str(e)}
    return results