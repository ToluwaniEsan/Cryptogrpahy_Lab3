# Cryptography Lab 3: Cascade Polyalphabetic Transposition Cipher (CPT)

## Overview

This project implements the **Cascade Polyalphabetic Transposition Cipher (CPT Cipher)** — a **multi-stage classical cipher** in Python:

1. **Length-keyed affine substitution** after removing spaces (`y = (a·x + b) mod 26`, with `a` invertible mod 26 and `b = n mod 26`).
2. **Vigenère encryption** on that stream (repeating keyword; non-letters in the key ignored).
3. **Rail Fence transposition** with **`rails ≥ 2`** (zigzag write, row-major read).
4. **Full string reverse** as a final permutation.

**Decryption** reverses those steps: un-reverse → Rail Fence decode → Vigenère decrypt → inverse affine.

Formal pseudocode: **[ALGORITHMS.md](ALGORITHMS.md)**. Readable notes: **[EXPLANATION.md](EXPLANATION.md)**.

## Features

- **Two substitution-style layers:** affine + Vigenère.
- **Two permutation-style layers:** Rail Fence + full reverse (meets typical “substitution + permutation” lab wording when both are required).
- **Public API:** `hybrid_encrypt` / `hybrid_decrypt`, plus `combined_hybrid_encrypt` / `combined_hybrid_decrypt` (inlined Vigenère, same results).
- **Utilities:** `custom_substitution_cipher`, `vigenere_encrypt`, `vigenere_decrypt` for building blocks.
- **Interactive menu** — keyword, then a **numeric “extra layer” key** (integer ≥ 2, default **3**); decrypt must reuse the **same keyword and same number**. Output is only **`Encryption:`** / **`Decryption:`** lines.

## Files

- **[cpt_cipher.py](cpt_cipher.py)** — CPT implementation and menu.
- **[cipher_bridge.py](cipher_bridge.py)** — JSON stdin/stdout adapter used by the Next.js API (imports `cpt_cipher` unchanged).
- **`web/`** — Next.js UI (gold / white / grey frosted layout) calling Python via `/api/cipher`.
- **[ALGORITHMS.md](ALGORITHMS.md)** — pseudocode only.
- **[EXPLANATION.md](EXPLANATION.md)** — short glossary and pipeline description.
- **[CPT_CIPHER_PRESENTATION_PROMPT.md](CPT_CIPHER_PRESENTATION_PROMPT.md)** — ready-to-paste prompt for Gamma (or similar) to generate class slides.
- **README.md** — this file.
- **`.gitignore`** — bytecode caches and Next.js build artifacts under `web/`.

## Mathematical summary

- **Affine:** `a = candidates[n mod 12]` from `(1, 3, …, 25)`, `b = n mod 26`; decrypt with `a⁻¹` mod 26.
- **Vigenère:** add/subtract key shifts mod 26; key index advances only on `A`–`Z` ciphertext letters.
- **Rail Fence / reverse:** see **[ALGORITHMS.md](ALGORITHMS.md)**.

## Running the program

```bash
python cpt_cipher.py
```

Self-check runs first, then the menu (Encrypt / Decrypt / Exit). When decrypting, use the **same keyword** and **same numeric key** (second number) as for encryption; empty numeric input defaults to **3** on both sides.

### Web UI (Next.js)

Requires **Node.js**, **npm**, and **Python 3** on your machine (the API runs `cipher_bridge.py`, which imports `cpt_cipher` from the repository root).

```bash
cd web
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). The dev server’s working directory is `web/`, so the API resolves the parent folder as the project root for Python.

- Override the Python executable with **`PYTHON_EXE`** (e.g. `py -3` on Windows) if `python` is not on `PATH`.
- If you start Next.js from a directory other than `web/`, set **`CIPHER_REPO_ROOT`** to the folder that contains **`cipher_bridge.py`** and **`cpt_cipher.py`**.

Serverless hosts (e.g. Vercel) typically **cannot** spawn a local Python interpreter; use this stack **locally** or deploy to a VM/container that has both Node and Python.


## Usage example

```python
from cpt_cipher import (
    hybrid_encrypt,
    hybrid_decrypt,
    combined_hybrid_encrypt,
    combined_hybrid_decrypt,
)

plain = "Hello World"
key = "KEY"
rails = 3

cipher = hybrid_encrypt(plain, key, rails)
assert cipher == combined_hybrid_encrypt(plain, key, rails)

recovered = hybrid_decrypt(cipher, key, rails)
assert recovered == combined_hybrid_decrypt(cipher, key, rails)
assert recovered == "HELLOWORLD"  # spaces not restored; Latin letters uppercase
```

## Edge cases and errors

- **`TypeError`**: wrong types for text/key where checked.
- **`ValueError`**: empty keyword after letter filtering; second parameter **< 2** or not a valid integer where a **numeric key** is read.
- **Spaces / case**: spaces stripped before encrypt and not restored; Latin letters decrypt to **uppercase**.

## Security note

Educational use only.

## Author

Cryptography Lab 3 - April 2026

## License

Educational use only.
