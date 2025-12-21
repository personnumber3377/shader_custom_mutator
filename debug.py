
# -----------------------------
# For debugging
# -----------------------------

DEBUG = False

def dlog(string):
    with open("custom_mutator.log", "a") as log:
        log.write(f"custom_mutator exception: {string}\n")

def dprint(msg: str) -> None:
    if DEBUG:
        print("[DEBUG] "+str(msg))
    return

