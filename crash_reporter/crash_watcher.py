#!/usr/bin/env python3
import os
import re
import time
import hashlib
import subprocess
import smtplib
from email.message import EmailMessage

# -----------------------
# CONFIG
# -----------------------

FUZZER = "./angle_translator_fuzzer"
SYMBOLIZER = "/usr/bin/llvm-symbolizer"

SCAN_INTERVAL = 10  # seconds

SEEN_DB = "seen_crashes.txt"
BANLIST = "ban_signatures.txt"

# Email config (SMTP)
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.environ["SMTP_USER"]
SMTP_PASS = os.environ["SMTP_PASS"] # "your_app_password"
EMAIL_TO = os.environ["EMAIL_TO"] # "your_email@gmail.com"

# -----------------------
# UTILS
# -----------------------

STACK_RE = re.compile(r"^\s*#([0-9]+)\s+.*$", re.MULTILINE)
ADDR_RE = re.compile(r"0x[0-9a-fA-F]+")

def load_set(path):
    if not os.path.exists(path):
        return set()
    return set(open(path).read().splitlines())

def save_set(path, s):
    with open(path, "w") as f:
        for x in sorted(s):
            f.write(x + "\n")

def normalize_stack(stderr: str) -> str:
    frames = []
    for line in stderr.splitlines():
        if line.strip().startswith("#"):
            line = ADDR_RE.sub("ADDR", line)
            frames.append(line)
        if len(frames) >= 5:
            break
    return "\n".join(frames)

def fingerprint(stderr: str) -> str:
    stack = normalize_stack(stderr)
    return hashlib.sha1(stack.encode()).hexdigest()

def is_interesting(stderr: str) -> bool:
    return ("Assertion" in stderr) or ("ERROR" in stderr)

def banned(stderr: str, banlist) -> bool:
    return any(b in stderr for b in banlist)

# -----------------------
# EMAIL
# -----------------------

def send_email(subject: str, body: str):
    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)

# -----------------------
# RUNNER
# -----------------------

def run_fuzzer(path: str) -> str:
    env = os.environ.copy()
    env["ASAN_OPTIONS"] = f"external_symbolizer_path={SYMBOLIZER}"

    p = subprocess.run(
        [FUZZER, path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        timeout=10,
    )

    return p.stderr.decode(errors="ignore")

# -----------------------
# MAIN LOOP
# -----------------------

def main():
    print("[*] Starting crash watcher")

    seen = load_set(SEEN_DB)
    banlist = load_set(BANLIST)

    while True:
        for fn in sorted(os.listdir(".")):
            if not fn.startswith("crash-"):
                continue

            try:
                stderr = run_fuzzer(fn)
            except Exception as e:
                print(f"[!] Failed running {fn}: {e}")
                continue

            if not is_interesting(stderr):
                continue

            if banned(stderr, banlist):
                print(f"[-] Banned crash: {fn}")
                continue

            sig = fingerprint(stderr)

            if sig in seen:
                continue

            seen.add(sig)
            save_set(SEEN_DB, seen)

            subject = "🔥 New ANGLE Crash Found"
            body = f"""
File: {fn}

Signature:
{sig}

Stack (normalized):
{normalize_stack(stderr)}

Full stderr:
{stderr}
"""

            print(f"[+] NEW CRASH: {fn}")
            send_email(subject, body)

        time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    main()