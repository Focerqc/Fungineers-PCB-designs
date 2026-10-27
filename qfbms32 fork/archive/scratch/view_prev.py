import json, sys

with open(r"C:\Users\quinn\.gemini\antigravity-ide\brain\dd3e1d3a-3b25-4800-9f81-37526309b7a2\.system_generated\logs\transcript.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        obj = json.loads(line)
        if obj.get("step_index") in [385]:
            sys.stdout.buffer.write(obj.get("content").encode('utf-8'))
