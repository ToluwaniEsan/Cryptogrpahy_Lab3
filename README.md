# Cryptography Lab 3: Substitution + Vigenere + Rail Fence hybrid

## Overview

This project implements a **multi-stage classical cipher** in Python:

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
- **Interactive menu** with **rails** prompt (default **3**); decrypt must use the **same key and rails** as encrypt.

## Files

- **[substitution_vigenere_cipher.py](substitution_vigenere_cipher.py)** — implementation and menu.
- **[ALGORITHMS.md](ALGORITHMS.md)** — pseudocode only.
- **[EXPLANATION.md](EXPLANATION.md)** — short glossary and pipeline description.
- **README.md** — this file.
- **`.gitignore`** — bytecode caches.

## Mathematical summary

- **Affine:** `a = candidates[n mod 12]` from `(1, 3, …, 25)`, `b = n mod 26`; decrypt with `a⁻¹` mod 26.
- **Vigenère:** add/subtract key shifts mod 26; key index advances only on `A`–`Z` ciphertext letters.
- **Rail Fence / reverse:** see **[ALGORITHMS.md](ALGORITHMS.md)**.

## Running the program

```bash
python substitution_vigenere_cipher.py
```

Self-check runs first, then the menu (Encrypt / Decrypt / Exit). For decrypt, enter the **same Vigenère key** and **same number of rails** used when encrypting.

## Usage example

```python
from substitution_vigenere_cipher import (
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
- **`ValueError`**: empty key after letter filtering; **`rails < 2`**; invalid integer for rails in the menu.
- **Spaces / case**: spaces stripped before encrypt and not restored; Latin letters decrypt to **uppercase**.

## Security note

Educational use only.

## Author

Cryptography Lab 3 - April 2026

## License

Educational use only.
