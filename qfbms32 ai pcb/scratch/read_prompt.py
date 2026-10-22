import json

with open(r"C:\Users\quinn\.gemini\antigravity-ide\brain\da94429c-ba52-43c3-a118-fc16f71395ae\.system_generated\logs\transcript.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        if '"USER_INPUT"' in line and "CRITICAL FOOTPRINT" in line:
            print("FOUND PROMPT:")
            print(json.loads(line).get("content"))
