#!/usr/bin/env python3
"""Report copies in reference/ whose origin has changed since they were synced.

Reads reference/sources.json. For each entry, asks the origin repo for the latest
commit touching origin_paths and compares it with synced_at_commit. Entries with
"compare": "content" (origins that aren't git repos) are compared byte for byte. Exit code 1 if
anything is stale, 0 otherwise. When an origin repo isn't on this machine (for
example a cloud agent that only has this repo), the entry is skipped, not failed.
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def latest_commit(repo, paths):
    out = subprocess.run(
        ["git", "-C", repo, "log", "-1", "--format=%h", "--", *paths],
        capture_output=True, text=True,
    )
    return out.stdout.strip() if out.returncode == 0 else None


def main():
    with open(os.path.join(ROOT, "reference", "sources.json")) as f:
        entries = json.load(f)
    stale = 0
    for e in entries:
        repo = os.path.expanduser(e["origin_repo"])
        if not os.path.isdir(repo):
            print(f"SKIP   {e['copy']}: origin {e['origin_repo']} not on this machine")
            continue
        if e.get("compare") == "content":
            # Origin isn't a git repo: compare the single file byte for byte.
            origin = os.path.join(repo, e["origin_paths"][0])
            copy = os.path.join(ROOT, e["copy"])
            if not os.path.isfile(origin):
                print(f"SKIP   {e['copy']}: {origin} not on this machine")
            elif open(origin, "rb").read() == open(copy, "rb").read():
                print(f"OK     {e['copy']} (matches {e['origin_repo']}/{e['origin_paths'][0]})")
            else:
                stale += 1
                print(f"STALE  {e['copy']}: differs from {e['origin_repo']}/{e['origin_paths'][0]}")
                print(f"       refresh: {e['how_to_refresh']}")
            continue
        head = latest_commit(repo, e["origin_paths"])
        if head is None:
            print(f"SKIP   {e['copy']}: could not read git history in {e['origin_repo']}")
        elif head.startswith(e["synced_at_commit"]) or e["synced_at_commit"].startswith(head):
            print(f"OK     {e['copy']} (origin at {head})")
        else:
            stale += 1
            print(f"STALE  {e['copy']}: synced at {e['synced_at_commit']}, origin now {head}")
            print(f"       refresh: {e['how_to_refresh']}")
    sys.exit(1 if stale else 0)


if __name__ == "__main__":
    main()
