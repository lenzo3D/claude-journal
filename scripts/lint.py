#!/usr/bin/env python3
"""House-rule check for the journal repo. Run before every commit.

Fails (exit 1) if any text file contains an em dash (U+2014) or something that
looks like a leaked secret. Written as a plain script, with no shell tricks, so
unattended runs can be allowed to call `python3 scripts/lint.py` without extra
permissions.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "fonts"}
TEXT_EXT = {".md", ".json", ".py", ".txt", ".yml", ".yaml", ".html", ".css", ".js"}
EM_DASH = "\u2014"
SECRETS = [
    ("API key (sk-)", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("Private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}\.")),
    ("Connection string", re.compile(r"\b(postgres|postgresql|mysql|mongodb(\+srv)?)://[^\s:/]+:[^\s@]+@")),
]


def main():
    problems = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if os.path.splitext(name)[1].lower() not in TEXT_EXT:
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, ROOT)
            try:
                with open(path, encoding="utf-8") as f:
                    lines = f.readlines()
            except (UnicodeDecodeError, OSError):
                continue
            for n, line in enumerate(lines, 1):
                if EM_DASH in line:
                    problems.append(f"{rel}:{n}: em dash")
                for label, pattern in SECRETS:
                    if pattern.search(line):
                        problems.append(f"{rel}:{n}: possible secret ({label})")
    if problems:
        print("\n".join(problems))
        print(f"\nlint: {len(problems)} problem(s). Fix them before committing.")
        sys.exit(1)
    print("lint: clean (no em dashes, no secret-looking strings)")


if __name__ == "__main__":
    main()
