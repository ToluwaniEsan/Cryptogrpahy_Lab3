#!/usr/bin/env python3
"""JSON stdin/stdout bridge for CPT cipher — imports cpt_cipher unchanged."""

from __future__ import annotations

import json
import sys

from cpt_cipher import hybrid_decrypt, hybrid_encrypt


def main() -> None:
    raw = sys.stdin.read()
    if len(raw) > 2_000_000:
        print(json.dumps({"ok": False, "error": "Payload too large"}))
        sys.exit(1)
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"ok": False, "error": f"Invalid JSON: {e}"}))
        sys.exit(1)

    mode = payload.get("mode")
    text = payload.get("text")
    key = payload.get("key")
    rails = payload.get("rails")

    if mode not in ("encrypt", "decrypt"):
        print(json.dumps({"ok": False, "error": 'mode must be "encrypt" or "decrypt"'}))
        sys.exit(1)
    if not isinstance(text, str) or not isinstance(key, str):
        print(json.dumps({"ok": False, "error": "text and key must be strings"}))
        sys.exit(1)
    if not isinstance(rails, int):
        print(json.dumps({"ok": False, "error": "rails must be an integer"}))
        sys.exit(1)

    try:
        if mode == "encrypt":
            result = hybrid_encrypt(text, key, rails)
        else:
            result = hybrid_decrypt(text, key, rails)
    except (TypeError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        sys.exit(1)

    print(json.dumps({"ok": True, "result": result}))


if __name__ == "__main__":
    main()
