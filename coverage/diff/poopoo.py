import json
from collections import defaultdict

def load_coverage(path):
    data = json.load(open(path))
    covered = defaultdict(set)

    for file in data["data"][0]["files"]:
        fname = file["filename"]
        for seg in file.get("segments", []):
            line, col, count, *_ = seg
            if count > 0:
                covered[fname].add(line)

    return covered

good = load_coverage("good.json")
single = load_coverage("single.json")

new = {}
for f in good:
    added = good[f] - single.get(f, set())
    if added:
        new[f] = added

print("Files with new coverage:", len(new))
total = sum(len(v) for v in new.values())
print("Total new lines:", total)
