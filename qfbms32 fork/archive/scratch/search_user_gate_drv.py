import os
import glob
import json

brain_base = r"C:\Users\quinn\.gemini\antigravity-ide\brain"
for log_file in glob.glob(os.path.join(brain_base, "*", ".system_generated", "logs", "transcript.jsonl")):
    with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "U_GATE_DRV" in line or "U_SSR1" in line:
                try:
                    data = json.loads(line)
                    if data.get("source") in ["USER_EXPLICIT", "USER_INPUT"]:
                        print(f"USER in {os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(log_file))))}:")
                        print(data.get("content")[:300])
                        print("-" * 50)
                except:
                    pass
