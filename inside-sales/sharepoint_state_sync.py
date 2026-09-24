#!/usr/bin/env python3
"""
Sync the Inside Sales dashboard's state files to/from SharePoint via Microsoft
Graph, using an app-only (client credentials) token. Replaces git as the
persistence mechanism for these files, since the scheduled runner cannot
commit/push.

Files bytes are streamed straight to/from the Graph API content endpoint -
they never pass through an LLM context window, so there is no size limit
issue (Graph's simple upload endpoint handles up to 4MB; every file here is
under 300KB).

Usage:
    python sharepoint_state_sync.py pull   # download the 8 files before refresh.py runs
    python sharepoint_state_sync.py push   # upload the 8 files after refresh.py runs

Requires AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET in the
environment. The app registration needs Sites.ReadWrite.All (or
Files.ReadWrite.All scoped to the target site), admin-consented.

Exit codes: 0 = success, 1 = config error, 2 = auth error, 3 = network/API error.
"""

import os
import sys

import requests

DRIVE_ID = "b!7bk81LOfLkOPkKWubDZGIDQ6IU0l1jBDvSHCSB5pI3EnVweU8dsHSplKSQPA60R1"
FOLDER_ID = "01HHADTSS4A6HX7YNZDJHJ5THS6PSSRJ5K"
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

STATE_FILES = [
    "vom_state.json",
    "summary.json",
    "sourced_pids.txt",
    "revenue.json",
    "voice_of_market.json",
    "vom_slim.json",
    "deals.json",
    "sources.json",
]


def get_token():
    tenant = os.environ.get("AZURE_TENANT_ID")
    client_id = os.environ.get("AZURE_CLIENT_ID")
    client_secret = os.environ.get("AZURE_CLIENT_SECRET")
    if not all([tenant, client_id, client_secret]):
        print("Missing AZURE_TENANT_ID / AZURE_CLIENT_ID / AZURE_CLIENT_SECRET in environment", file=sys.stderr)
        sys.exit(1)

    resp = requests.post(
        f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token",
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "https://graph.microsoft.com/.default",
        },
        timeout=30,
    )
    if resp.status_code != 200:
        print(f"Auth failed: HTTP {resp.status_code} {resp.text[:500]}", file=sys.stderr)
        sys.exit(2)
    return resp.json()["access_token"]


def pull(token):
    headers = {"Authorization": f"Bearer {token}"}
    failures = []
    for fname in STATE_FILES:
        url = f"https://graph.microsoft.com/v1.0/drives/{DRIVE_ID}/items/{FOLDER_ID}:/{fname}:/content"
        resp = requests.get(url, headers=headers, timeout=120)
        if resp.status_code == 404:
            print(f"  {fname}: not found on SharePoint yet, skipping (first run)")
            continue
        if resp.status_code != 200:
            print(f"  {fname}: FAILED HTTP {resp.status_code} {resp.text[:300]}", file=sys.stderr)
            failures.append(fname)
            continue
        local_path = os.path.join(DATA_DIR, fname)
        with open(local_path, "wb") as f:
            f.write(resp.content)
        print(f"  {fname}: pulled ({len(resp.content)} bytes)")
    if failures:
        print(f"pull: {len(failures)} file(s) failed: {failures}", file=sys.stderr)
        sys.exit(3)


def push(token):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/octet-stream"}
    failures = []
    for fname in STATE_FILES:
        local_path = os.path.join(DATA_DIR, fname)
        if not os.path.exists(local_path):
            print(f"  {fname}: local file missing, skipping", file=sys.stderr)
            failures.append(fname)
            continue
        size = os.path.getsize(local_path)
        url = f"https://graph.microsoft.com/v1.0/drives/{DRIVE_ID}/items/{FOLDER_ID}:/{fname}:/content"
        with open(local_path, "rb") as f:
            resp = requests.put(url, headers=headers, data=f, timeout=120)
        if resp.status_code not in (200, 201):
            print(f"  {fname}: FAILED HTTP {resp.status_code} {resp.text[:300]}", file=sys.stderr)
            failures.append(fname)
            continue
        remote_size = resp.json().get("size")
        ok = remote_size == size
        print(f"  {fname}: pushed ({remote_size} bytes) {'OK' if ok else 'SIZE MISMATCH'}")
        if not ok:
            failures.append(fname)
    if failures:
        print(f"push: {len(failures)} file(s) failed or mismatched: {failures}", file=sys.stderr)
        sys.exit(3)


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("pull", "push"):
        print(__doc__)
        sys.exit(1)

    token = get_token()
    if sys.argv[1] == "pull":
        print("Pulling state files from SharePoint...")
        pull(token)
    else:
        print("Pushing state files to SharePoint...")
        push(token)
    print("Done.")


if __name__ == "__main__":
    main()
