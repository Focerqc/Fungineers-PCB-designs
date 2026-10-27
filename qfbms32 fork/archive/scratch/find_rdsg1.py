import json

with open(r"C:\Users\quinn\.gemini\antigravity-ide\brain\dd3e1d3a-3b25-4800-9f81-37526309b7a2\.system_generated\logs\transcript.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        if "R_DSG1" in line:
            obj = json.loads(line)
            print("Step:", obj.get("step_index"))
            if "tool_calls" in obj:
                print("Tool call:", obj["tool_calls"])
