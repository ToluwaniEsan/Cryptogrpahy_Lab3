# Explanation (readable overview)

The exact pseudocode lives in **[ALGORITHMS.md](ALGORITHMS.md)**. This page gives short definitions and a bird’s-eye view of [**substitution_vigenere_cipher.py**](substitution_vigenere_cipher.py)—enough to read the lab without drowning in detail.

---

## Keywords (what the words usually mean)

**Affine cipher** — In cryptography, a substitution where each letter (as a number 0–25) is transformed by a **linear rule** `y = (a·x + b) mod m`. “Affine” means linear (scale by `a`, shift by `b`). Our `m` is **26** (the Latin alphabet).

**Unit / invertible modulo 26** — A number `a` is usable as the multiplier only if decryption can undo it: there must exist `a⁻¹` with `(a·a⁻¹) mod 26 = 1`. That works when `a` shares no factors with 26 (odd and not divisible by **13**). Our code picks `a` from a fixed list of such values.

**Modular inverse** — For a fixed modulus (here **26**), `a⁻¹` is the integer in `1…25` that “undoes” multiplication by `a` modulo 26. The program finds it by trial; see `MODULAR_INVERSE` in ALGORITHMS.md.

**Vigenère cipher** — A polyalphabetic cipher: you **add** a repeating key letter (as a shift 0–25) to each plaintext letter modulo 26. Decrypting **subtracts** the same shift. Non-letters don’t use a key letter and don’t advance the key position.

**Plaintext / ciphertext** — Plaintext is the message you start from; ciphertext is the scrambled output. Here, “substitution output” is an intermediate string between the two stages.

**Key (sanitized)** — The user types any string; the program **keeps only `A`–`Z`**, in order, uppercased. If nothing is left, encryption/decryption cannot run and the program raises an error.

---

## How the whole thing works

**Input.** You give a **phrase** and a **keyword**. Spaces are **removed** from the phrase (they are not encrypted and are **lost**). Only ASCII **`A`–`Z`** are encrypted; digits and punctuation are copied through both stages unchanged.

**Stage 1 — substitution.**  
Let `n` be the length of the space-free string. The program chooses `a` from a length-dependent list and sets `b = n mod 26`. Each letter `A`–`Z` becomes another letter using the affine rule on indices 0–25. Result: an uppercase Latin stream (with other characters unchanged).

**Stage 2 — Vigenère.**  
That stream is mixed again: each `A`–`Z` is shifted forward by the current key letter; the key **repeats** when it runs out. Only letter positions consume key letters.

**Decrypt.**  
Run **backward**: undo Vigenère (subtract shifts), then undo the affine map with the **same** `n`, `a`, and `b` derived from the ciphertext length (which equals the old `n`).

**What the code checks.**  
- Arguments that must be strings use `isinstance(..., str)` where relevant.  
- The Vigenère key must contain **at least one** letter after stripping non-letters.  
- Invalid modular inverse should not happen for our fixed `a` values; if it did, you’d get a clear error.

**Running as a script.**  
A quick self-test runs first; then the menu lets you **encrypt**, **decrypt**, or **exit**. Decrypt prints the recovered text **without spaces** and with Latin letters in **uppercase**.

---

## Spec vs. this code

The behavior matches **[ALGORITHMS.md](ALGORITHMS.md)**. The implementation identifies letters with a small helper so only plain ASCII `A`–`Z` are treated as alphabet letters (many symbols of other alphabets are left as-is rather than run through `str.upper()` globally). For typical English input, that matches “remove spaces, uppercase letters, encrypt.”
