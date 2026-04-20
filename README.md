# Cryptography Lab 3: Substitution + Vigenere hybrid

## Overview

This project implements a **two-stage classical cipher** in Python:

1. **Length-keyed affine substitution** on the message with all spaces removed. Letters `A`–`Z` are mapped with `y = (a·x + b) mod 26` (with `x,y` in `0..25`), where `a` is chosen from fixed units modulo 26 so **decryption always exists**, and `b = n mod 26` for `n =` length of the cleaned string. Non-letters pass through unchanged.

2. **Vigenere encryption** on the substitution output, using a repeating keyword (letters `A`–`Z` only; other characters in the key are ignored).

**Decryption** reverses that order: Vigenere decrypt, then inverse substitution. You can use either a **pipeline** of functions or **combined** encrypt/decrypt helpers.

Formal pseudocode (same style as the lab PDF): **[ALGORITHMS.md](ALGORITHMS.md)**. Optional notes tying the spec to the script: **[EXPLANATION.md](EXPLANATION.md)**.

## Features

- **Substitution stage**: affine cipher over `Z/26Z` with length-dependent `a` and `b`; always invertible for any message length (no `gcd(n, 26)` restriction).
- **Vigenere stage**: standard additive cipher over `A`–`Z`; the key index advances only for ciphertext letters that are encrypted (non-letters pass through and do not consume key material).
- **Decrypt API**: `vigenere_decrypt`, `decrypt_substitution_then_vigenere`, `combined_substitution_vigenere_decrypt` (combined decrypt does not call `vigenere_decrypt`; it mirrors the encrypt structure).
- **Two API styles** for encrypt: `custom_substitution_cipher` + `vigenere_encrypt`, or `combined_substitution_vigenere_encrypt`.
- **Interactive menu** (`python substitution_vigenere_cipher.py`): choose **Encrypt**, **Decrypt**, or **Exit**; after each result you return to the menu until you exit.
- **Robust letter handling**: only ASCII `A`–`Z` are transformed; other Unicode letters are copied unchanged so behavior stays predictable for coursework.

## Files

- **[substitution_vigenere_cipher.py](substitution_vigenere_cipher.py)**: affine substitution, Vigenere, combined encrypt/decrypt, interactive menu (replaces the older `substitution.py` prototype).
- **[ALGORITHMS.md](ALGORITHMS.md)**: `ENCRYPT`, `DECRYPT`, `MODULAR_INVERSE`, and utility definitions (pseudocode only).
- **[EXPLANATION.md](EXPLANATION.md)**: short notes on how the spec maps to the Python implementation (optional).
- **README.md**: This file.
- **`.gitignore`**: ignores Python bytecode caches.

See **[ALGORITHMS.md](ALGORITHMS.md)** for full symbolic steps. Summary:

### Substitution (after removing spaces)

Let `n` be the length of the cleaned string, `x` the numerical value of a plaintext letter (`A`→0, …, `Z`→25). Pick multiplier `a = candidates[n mod 12]` from `(1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)` (all units mod 26). Let `b = n mod 26`.

`y = (a·x + b) mod 26`, then map `y` back to `A`–`Z`.

Decryption: `x = (a⁻¹·(y − b)) mod 26` where `a⁻¹` is the modular inverse of `a` modulo 26.

If `n == 0`, the result is the empty string.

### Vigenere

Encryption: `C = chr((ord(P) - 65 + ord(K) - 65) mod 26 + 65)`.

Decryption: `P = chr((ord(C) - 65 - ord(K) - 65) mod 26 + 65)` (same key stepping as encrypt).

## Running the program

```bash
python substitution_vigenere_cipher.py
```

On startup a small **self-check** runs (round-trip for a sample message, including length 10). Then you see a menu:

1. **Encrypt** — enter phrase and key; prints substitution-only output, pipeline ciphertext, blended ciphertext, and whether encrypt paths match.
2. **Decrypt** — enter ciphertext and key; prints recovered text (**spaces are not restored**; letter case is uppercase for Latin letters). Also reports whether combined decrypt matches the pipeline.
3. **Exit** — quit the program.

You can also type `encrypt` / `decrypt` / `exit` (case-insensitive) instead of `1` / `2` / `3`.

## Usage example

```python
from substitution_vigenere_cipher import (
    encrypt_substitution_then_vigenere,
    decrypt_substitution_then_vigenere,
    combined_substitution_vigenere_encrypt,
    combined_substitution_vigenere_decrypt,
)

plain = "Hello World"
key = "KEY"

cipher = encrypt_substitution_then_vigenere(plain, key)
assert cipher == combined_substitution_vigenere_encrypt(plain, key)

recovered = decrypt_substitution_then_vigenere(cipher, key)
assert recovered == combined_substitution_vigenere_decrypt(cipher, key)
assert recovered == "HELLOWORLD"  # spaces not restored; Latin letters uppercase
```

## Edge cases and errors

- **`TypeError`**: `text`, `ciphertext`, or `key` is not a `str` where a string is required.
- **`ValueError`**: Vigenere key contains no `A`–`Z` letters after sanitizing (or internal modular inverse failure, which should not occur for the fixed `a` values).
- **Empty input**: Produces empty ciphertext; substitution length `n` is zero.
- **Spaces and case**: Spaces are removed before encryption and are **not** recovered on decrypt. Latin letters are recovered in **uppercase**.

## Security note

This code is **for education only**. Classical ciphers are not suitable for protecting real data.

## Author

Cryptography Lab 3 - April 2026

## License

Educational use only.
