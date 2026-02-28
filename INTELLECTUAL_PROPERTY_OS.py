"""
INTELLECTUAL PROPERTY OS
========================

Protects:
- Python research code
- Lean formalization
- Coq formal proofs

Functions:
- File hashing (SHA256)
- Timestamp generation
- Ownership declaration
- License auto-generation
- Evidence record archive

Fully executable.
"""

import os
import hashlib
import datetime
import json

OWNER = "Suzuki Yukiya"
PROJECT_NAME = "H1 Golden Discrepancy Theory"
LICENSE_TYPE = "Dual License (Research Open + Commercial Restricted)"


# ============================================================
# 1. Hashing Engine
# ============================================================

def hash_file(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


def hash_directory(directory):
    records = {}
    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            records[path] = hash_file(path)
    return records


# ============================================================
# 2. Timestamp Record
# ============================================================

def generate_timestamp():
    return datetime.datetime.utcnow().isoformat() + "Z"


# ============================================================
# 3. Ownership Declaration
# ============================================================

def generate_declaration(hashes):
    declaration = {
        "owner": OWNER,
        "project": PROJECT_NAME,
        "timestamp_utc": generate_timestamp(),
        "license": LICENSE_TYPE,
        "file_hashes": hashes,
        "statement": "All original mathematical structures, algorithms, and formal systems contained herein are claimed as intellectual creation of the owner."
    }
    return declaration


# ============================================================
# 4. License Generator
# ============================================================

def generate_license_text():
    return f"""
{PROJECT_NAME}
Copyright (c) {datetime.datetime.utcnow().year} {OWNER}

This project is dual-licensed:

1. Research License:
   Free for academic and non-commercial use with citation.

2. Commercial License:
   Explicit written permission required from the owner.

Unauthorized commercial exploitation prohibited.
"""


# ============================================================
# 5. Save Records
# ============================================================

def save_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def save_text(text, filename):
    with open(filename, "w") as f:
        f.write(text)


# ============================================================
# 6. Full IP Protection Pipeline
# ============================================================

def protect_project(target_directory="."):

    print("Scanning project files...")
    hashes = hash_directory(target_directory)

    print("Generating ownership declaration...")
    declaration = generate_declaration(hashes)

    print("Saving records...")
    save_json(declaration, "IP_Declaration.json")
    save_text(generate_license_text(), "LICENSE.txt")

    print("IP protection package generated.")
    print("Files created:")
    print(" - IP_Declaration.json")
    print(" - LICENSE.txt")


# ============================================================
# 7. Main
# ============================================================

if __name__ == "__main__":
    protect_project()
