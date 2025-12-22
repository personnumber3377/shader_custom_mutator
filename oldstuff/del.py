import os

for f in os.listdir("."):
    if os.path.isfile(f) and len(f) == 40:
        print("Deleting:", f)
        os.remove(f)
