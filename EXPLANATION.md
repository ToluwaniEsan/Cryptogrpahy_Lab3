# Explanation (readable overview)

The canonical step-by-step math is **[ALGORITHMS.md](ALGORITHMS.md)**. This file summarizes [**substitution_vigenere_cipher.py**](substitution_vigenere_cipher.py): what each layer does, how parameters line up with the interactive prompts, and how substitution differs from permutation.

---

## Keywords (what the words usually mean)

**Affine cipher** — Substitution on letter indices using a linear rule modulo 26: scale by `a`, add `b`, both derived from message length.

**Vigenère cipher** — Polyalphabetic substitution: each `A`–`Z` letter is shifted by the current keyword letter (mod 26); decrypt subtracts that shift. Non-letters do not consume keyword letters.

**Rail Fence cipher** — **Transposition:** the string is laid out in a zigzag across **`r`** horizontal rows (`r ≥ 2`), then read row-by-row. Characters move position; values at each step come from prior layers.

**Full-string reverse** — **Transposition:** reverses character order end-to-end.

**Substitution vs permutation** — Substitution **replaces** symbols (affine, Vigenère). Permutation **reorders** positions (Rail Fence, reverse).

**Keyword (`K`)** — The alphabetic secret the user types; only `A`–`Z` are kept, in order. At least one letter is required.

**Numeric second parameter (`r` / `rails`)** — An integer **`≥ 2`** that fixes the Rail Fence geometry (how many rails). It is **not** part of Vigenère; it must match between encrypt and decrypt. The code names this argument **`rails`**; the menu calls it a **numeric key for the extra layer** so it is clearly separate from the keyword.

---

## End-to-end pipeline

**Encrypt:** strip spaces → affine substitution → Vigenère → Rail Fence using **`r`** rows → reverse entire string.

**Decrypt:** reverse → Rail Fence decode with the **same `r`** → Vigenère decrypt → inverse affine.

**What changes per letter:** Affine and Vigenère only alter ASCII **`A`–`Z`** (treated as uppercase). Other characters are unchanged by those two layers but still move under Rail Fence and reverse.

**Validation:** Inputs are checked where needed (`str` types); keyword must retain at least one letter after filtering; **`r` must be ≥ 2** (implementation messages may say **“Numeric key…”**).

---

## Interactive program (`python substitution_vigenere_cipher.py`)

1. A **self-check** runs once at startup (round-trip on a sample message).  
2. The menu offers **Encrypt**, **Decrypt**, or **Exit**.  
3. **Encrypt** asks for: phrase → **keyword** → **numeric key** for the extra layer (whole number ≥ 2; empty input means **3**). It prints a single line: **`Encryption: '…'`**.  
4. **Decrypt** asks for: ciphertext → **same keyword** → **same numeric key** (empty = 3). It prints **`Decryption: '…'`** (space-free, Latin letters uppercase).  

No intermediate pipeline or “blended match” lines are shown—only the final ciphertext or recovered plaintext.

---

## Spec vs this code

Behavior matches **[ALGORITHMS.md](ALGORITHMS.md)**. Letter handling uses a helper so only plain ASCII **`A`–`Z`** count as alphabet letters for affine and Vigenère (consistent with `FILTER_LETTERS` / uppercasing in the spec).
