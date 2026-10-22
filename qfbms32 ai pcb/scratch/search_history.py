import os
import glob
import json

brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain"
transcripts = glob.glob(os.path.join(brain_dir, "*", ".system_generated", "logs", "transcript.jsonl"))

for t in sorted(transcripts, key=os.path.getmtime, reverse=True)[:5]:
    conv_id = t.split(os.sep)[-4]
    print(f"=== Conversation {conv_id} ===")
    with open(t, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if '"USER_INPUT"' in line:
                try:
                    data = json.loads(line)
                    content = data.get("content", "")
                    if any(w in content.lower() for w in ["xt30", "lug", "drill", "tab", "q1", "toll", "pad"]):
                        print("USER:", content[:300].strip())
                        print("-" * 40)
                except:
                    pass
