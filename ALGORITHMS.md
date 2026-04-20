# Encryption

1. Let `clean` be the input string with every space (`U+0020`) removed. Let `n = len(clean)`.

2. Only characters that are ASCII `A`–`Z` are transformed (case-normalize to uppercase first). Index letters as `x ∈ {0,…,25}` with `A ↦ 0`, …, `Z ↦ 25`. All other characters are copied unchanged at every stage.

3. **Substitution:**  
   Let `candidates = (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)`.  
   `a = candidates[n mod 12]`  
   `b = n mod 26`  
   For each letter with index `x`:  
   `y = (a·x + b) mod 26`  
   Output the letter with index `y`.

4. **Vigenère** on the substitution output:  
   Let `key_letters` be the user key stripped to ASCII `A`–`Z` only, uppercase, preserving order (must be non-empty). Let `key_len = len(key_letters)`. Maintain `key_index`, initially `0`.  
   For each character `c` in the string:
   - If `c` is ASCII `A`–`Z` with index `p`: let `k` be the index of `key_letters[key_index mod key_len]` (`0…25`).  
     `cipher_index = (p + k) mod 26`  
     Emit that letter; then `key_index ← key_index + 1`.
   - Else emit `c` unchanged (do not advance `key_index`).

The final string after step 4 is the ciphertext.

---

# Decryption

1. Let `cipher` be the ciphertext string from encryption. Its length equals `n` above (same as cleaned plaintext length).

2. **Vigenère inverse:**  
   Build `key_letters` exactly as in encryption from the user key.  
   `key_index ← 0`.  
   For each character `c`:
   - If `c` is ASCII `A`–`Z` with index `q`: let `k` be the index of `key_letters[key_index mod key_len]`.  
     `plain_index = (q − k) mod 26`  
     Emit that letter; then `key_index ← key_index + 1`.
   - Else emit `c` unchanged (do not advance `key_index`).

3. **Inverse substitution** on that string (same `n = len(cipher)`):  
   `a = candidates[n mod 12]` (same tuple as encryption)  
   `b = n mod 26`  
   Find integer `a_inv ∈ {1,…,25}` such that `(a · a_inv) mod 26 = 1`.  
   For each letter with index `y`:  
   `x = (a_inv · (y − b)) mod 26`  
   Emit the letter with index `x`. Non-letters unchanged.

The result is the recovered space-free plaintext (uppercase for Latin letters that were letters in the original).
