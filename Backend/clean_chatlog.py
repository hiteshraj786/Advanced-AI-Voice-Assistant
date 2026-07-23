# clean_chatlog.py
import json, os, shutil

DATA = os.path.join("Data", "ChatLog.json")
BAK = os.path.join("Data", "ChatLog.json.bak")
os.makedirs("Data", exist_ok=True)
if not os.path.exists(DATA):
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump([], f)

# backup
shutil.copy(DATA, BAK)

with open(DATA, "r", encoding="utf-8") as f:
    try:
        data = json.load(f)
    except Exception:
        data = []

cleaned = []
removed = 0
for m in data:
    content = (m.get("content") or "").strip()
    # remove any system messages that start with "The search results for"
    if m.get("role") == "system" and content.startswith("The search results for"):
        removed += 1
        continue
    cleaned.append(m)

with open(DATA, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, indent=4, ensure_ascii=False)

print("Backup created at:", BAK)
print("Removed", removed, "old search-result messages.")
