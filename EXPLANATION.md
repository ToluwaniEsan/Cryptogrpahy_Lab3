# Explanation (readable overview)

The exact pseudocode is **[ALGORITHMS.md](ALGORITHMS.md)**. This page summarizes [**substitution_vigenere_cipher.py**](substitution_vigenere_cipher.py) without repeating every formula.

---

## Keywords (what the words usually mean)

**Affine cipher** — Substitution using a linear rule on letter indices: `y = (a·x + b) mod 26`.

**Vigenère cipher** — Polyalphabetic substitution: add a repeating key shift (mod 26) per letter; decrypt subtracts the shift. Non-letters skip the key stream.

**Rail Fence cipher** — **Transposition:** characters are written in a zigzag across several horizontal “rails,” then read off row-by-row. Order changes; symbols stay the same until earlier stages changed them.

**Reverse (full string)** — **Transposition:** position `i` swaps with position `length − 1 − i`. Another reordering layer.

**Substitution vs permutation** — **Substitution** replaces symbols (affine, Vigenère). **Permutation** reorders positions (Rail Fence, reverse).

**Sanitized key** — Only ASCII `A`–`Z` from the typed keyword, in order; at least one letter required.

---

## How the pipeline works

**Encrypt chain:** remove spaces → affine substitution → Vigenère → Rail Fence (**`rails`** ≥ 2) → reverse entire string.

**Decrypt chain (inverse order):** reverse → Rail Fence decode → Vigenère decrypt → inverse affine.

You must use the **same** Vigenère key **and** the **same `rails`** value when decrypting. Default in the menu is **`rails = 3`** if you press Enter.

**What gets transformed:** Affine and Vigenère affect only ASCII **`A`–`Z`** (normalized to uppercase). Digits and punctuation pass through those stages unchanged but are still permuted by Rail Fence and reverse.

**Checks:** string types where required; key must retain at least one letter; **`rails ≥ 2`**; modular inverse for fixed `a` values should always exist.

**Script:** A self-test runs at startup; the menu prompts for encrypt/decrypt/exit, and for **rails** on encrypt and decrypt.

---

## Spec vs this code

Matches **[ALGORITHMS.md](ALGORITHMS.md)**. Letter detection uses a helper so only plain ASCII `A`–`Z` are treated as alphabet letters for the substitution and Vigenère steps.
