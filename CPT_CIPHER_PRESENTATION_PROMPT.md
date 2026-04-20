# Cascade Polyalphabetic Transposition Cipher (CPT Cipher) — Gamma presentation prompt

Copy everything **below the next horizontal rule** into Gamma AI.

---

Create a professional classroom presentation for a university **cryptography group project**. The deck should be clear for non-experts but technically accurate. Use the official cipher name and tie every slide back to the assignment requirements.

## Official cipher name

**Cascade Polyalphabetic Transposition Cipher (CPT Cipher)**

Short tagline suggestion: *“Multiple substitution and transposition layers in one pipeline.”*

## Assignment requirements (must be visibly addressed)

1. **Design and implement** a custom encryption algorithm (implementation exists in **Python**).
2. The algorithm must **uniquely combine two operations: substitution and permutation**.
3. It should include **multiple rounds of both substitution and permutation**.
4. **Distinctive name** reflecting the technique — use **CPT Cipher** above.
5. Present the **algorithm** and a **functioning program** (demo / menu).

### How CPT satisfies the rubric (use this framing on 1–2 slides)

**Substitution (two distinct rounds, applied in sequence — “cascade”):**

1. **Round 1 — Affine substitution** on the space-stripped message: letters `A`–`Z` mapped with `y = (a·x + b) mod 26`, where `x,y ∈ {0,…,25}`, `a` is chosen from a fixed list of values coprime to 26 (so decryption always exists), and `b = n mod 26` for message length `n`.
2. **Round 2 — Vigenère (polyalphabetic substitution)** on the output of round 1: each letter is shifted by a repeating keyword (mod 26); non-letters pass through without consuming key letters.

**Permutation (two distinct rounds, applied after substitution — “transposition”):**

3. **Round 3 — Rail Fence cipher**: the entire string (after substitution layers) is written in a zigzag across `r` horizontal rails (`r ≥ 2`), then read row-by-row — **reorders** characters.
4. **Round 4 — Full string reverse**: the ciphertext is reversed end-to-end — **another reordering** (transposition).

**Decrypt** runs the **inverse** of each step in **reverse order**: un-reverse → Rail Fence decode → Vigenère decrypt → inverse affine.

**“Polyalphabetic”** in the name refers to **Vigenère** (many alphabets via the keyword). **“Transposition”** refers to **Rail Fence + reverse**. **“Cascade”** refers to **stacked layers** left-to-right on encrypt.

## Keys and parameters (two pieces of secret / agreed material)

- **Keyword `K`** — Vigenère key; only ASCII `A`–`Z` from the string are used, in order (non-letters stripped). At least one letter required.
- **Numeric parameter `r` (code name: `rails`)** — integer **≥ 2**; controls Rail Fence depth. Default **3** in the program if the user presses Enter. Must match between encrypt and decrypt.

**Note:** Spaces are removed before encryption and are **not** recovered; Latin letters decrypt to **uppercase**.

## Implementation (for “functioning program” slides)

- **Language:** Python 3.
- **Main file:** `substitution_vigenere_cipher.py` (contains the full CPT pipeline and interactive menu).
- **Supporting docs in repo:** `ALGORITHMS.md` (full pseudocode: ENCRYPT, DECRYPT, RAIL_FENCE_ENCODE, RAIL_FENCE_DECODE, REVERSE, MODULAR_INVERSE, utilities), `EXPLANATION.md` (readable overview), `README.md`.

### Public API (mention on architecture slide)

| Function | Role |
|----------|------|
| `hybrid_encrypt(plaintext, key, rails=3)` | Full encrypt pipeline |
| `hybrid_decrypt(ciphertext, key, rails=3)` | Full decrypt pipeline |
| `combined_hybrid_encrypt` / `combined_hybrid_decrypt` | Same I/O as above; Vigenère step inlined (teaching / parity check) |
| `custom_substitution_cipher` | Affine-only (after strip spaces) |
| `vigenere_encrypt` / `vigenere_decrypt` | Vigenère-only building blocks |

### Important internal helpers (optional “under the hood” slide)

`_substitution_on_clean`, `_substitution_inverse_on_clean`, `_safe_multiplier`, `_mod_inverse`, `_sanitized_vigenere_key`, `_vigenere_apply`, `_vigenere_decrypt`, `_rail_fence_encode`, `_rail_fence_decode`, `_rail_pattern_indices`, `_reverse_layer`, `_as_latin_upper_letter`, `_self_check_round_trip`, `_run_menu`, `_parse_rails_input`.

### High-level encrypt pseudocode (ENCRYPT — for one slide or appendix)

1. Remove spaces, uppercase; `n` = length.  
2. Affine: `a = candidates[n mod 12]`, `b = n mod 26`; for each `A`–`Z`, `y = (a·x + b) mod 26`.  
3. Vigenère on result with keyword `K`.  
4. `R = RAIL_FENCE_ENCODE(S, r)`.  
5. `C = REVERSE(R)`. Return `C`.

Decrypt: `R = REVERSE(C)` → `S = RAIL_FENCE_DECODE(R, r)` → Vigenère decrypt → inverse affine.

### Demo / program behavior (for live or screenshot slide)

- Run: `python substitution_vigenere_cipher.py`.
- Self-check runs once at startup.
- Menu: **Encrypt** / **Decrypt** / **Exit**.
- Encrypt prompts: phrase → **keyword** → **numeric key for the extra layer** (this is `r`; Enter = 3). Output line: **`Encryption: '...'`**.
- Decrypt prompts: ciphertext → **same keyword** → **same numeric key**. Output: **`Decryption: '...'`**.

## Suggested slide outline (adapt as needed)

1. Title — CPT Cipher + team name + course.  
2. Assignment mapping — checklist: substitution + permutation + multiple rounds + implementation + presentation.  
3. What “cascade / polyalphabetic / transposition” means in **our** design.  
4. Encrypt pipeline diagram (4 boxes: Affine → Vigenère → Rail Fence → Reverse).  
5. Decrypt pipeline (reverse order).  
6. Substitution detail — affine formula + why `a` is invertible mod 26.  
7. Substitution detail — Vigenère (key stream, non-letters).  
8. Permutation detail — Rail Fence zigzag (use `r` rails).  
9. Permutation detail — full reverse.  
10. Keys — keyword + numeric `r`; what must match on decrypt.  
11. Python module + main functions table.  
12. Pseudocode excerpt or screenshot reference to `ALGORITHMS.md`.  
13. Demo — menu flow or example plaintext/ciphertext (short example).  
14. Limitations — educational only; spaces lost; classical security.  
15. Q&A.

## Visual / tone instructions for Gamma

- Use a **clean, academic** theme; one **pipeline diagram** for encrypt and one for decrypt.  
- Prefer **bullet points** over dense paragraphs on slides.  
- Include **one small numeric walk-through** (e.g. 4–6 letters) only if space allows, or skip to avoid clutter.  
- Do **not** claim military-grade security; state **educational prototype**.

---

End of prompt — generate the full presentation from the above.
