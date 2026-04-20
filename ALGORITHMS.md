# Hybrid Substitution–Vigenère–Rail Fence Cipher (Algorithm Specification)

**Parameters**

- `P` — plaintext string.  
- `K` — Vigenère **keyword** (only `A`–`Z` are used, in order, after uppercasing).  
- `r` (also written **`rails` in code**) — integer **≥ 2** that sets how many horizontal **rows** the Rail Fence zigzag uses. The same `r` is required to decrypt. In the interactive program this is the second, **numeric** input (default `3` if the user presses Enter). It is not the Vigenère keyword.

**Output** — Ciphertext `C` after, in order: affine substitution on the space-free text, Vigenère, Rail Fence with `r` rows, then **reversal** of the full string.

---

### ALGORITHM: ENCRYPT(P, K, r)

```
1.  clean ← REMOVE_SPACES(P)
2.  clean ← TO_UPPERCASE(clean)
3.  n ← LENGTH(clean)
4.  candidates ← (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)
5.  a ← candidates[n mod 12]
6.  b ← n mod 26
7.  T ← empty string
8.  for each character c in clean do
9.      if c ∈ {A, …, Z} then
10.         x ← ORD(c) − ORD('A')
11.         y ← (a·x + b) mod 26
12.         T ← T + CHAR(y + ORD('A'))
13.     else
14.         T ← T + c
15.     end if
16. end for
17. key_letters ← FILTER_LETTERS(K)
18. key_letters ← TO_UPPERCASE(key_letters)
19. key_len ← LENGTH(key_letters)
20. key_index ← 0
21. S ← empty string
22. for each character c in T do
23.     if c ∈ {A, …, Z} then
24.         p ← ORD(c) − ORD('A')
25.         k ← ORD(key_letters[key_index mod key_len]) − ORD('A')
26.         cipher_index ← (p + k) mod 26
27.         S ← S + CHAR(cipher_index + ORD('A'))
28.         key_index ← key_index + 1
29.     else
30.         S ← S + c
31.     end if
32. end for
33. R ← RAIL_FENCE_ENCODE(S, r)
34. C ← REVERSE(R)
35. return C
```

---

### ALGORITHM: DECRYPT(C, K, r)

```
1.  R ← REVERSE(C)
2.  S ← RAIL_FENCE_DECODE(R, r)
3.  n ← LENGTH(S)
4.  key_letters ← FILTER_LETTERS(K)
5.  key_letters ← TO_UPPERCASE(key_letters)
6.  key_len ← LENGTH(key_letters)
7.  key_index ← 0
8.  T ← empty string
9.  for each character c in S do
10.     if c ∈ {A, …, Z} then
11.         q ← ORD(c) − ORD('A')
12.         k ← ORD(key_letters[key_index mod key_len]) − ORD('A')
13.         plain_index ← (q − k) mod 26
14.         T ← T + CHAR(plain_index + ORD('A'))
15.         key_index ← key_index + 1
16.     else
17.         T ← T + c
18.     end if
19. end for
20. candidates ← (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)
21. a ← candidates[n mod 12]
22. b ← n mod 26
23. a_inv ← MODULAR_INVERSE(a, 26)
24. P′ ← empty string
25. for each character c in T do
26.     if c ∈ {A, …, Z} then
27.         y ← ORD(c) − ORD('A')
28.         x ← (a_inv · (y − b)) mod 26
29.         P′ ← P′ + CHAR(x + ORD('A'))
30.     else
31.         P′ ← P′ + c
32.     end if
33. end for
34. return P′
```

---

### ALGORITHM: RAIL_FENCE_ENCODE(text, r)

Requires integer **`r ≥ 2`**. Write each character of `text` along a zigzag across **`r`** rows (bounce at top and bottom rows). Concatenate row 0, then row 1, …, row **`r − 1`** (left to right within each row).

---

### ALGORITHM: RAIL_FENCE_DECODE(cipher, r)

Requires **`r ≥ 2`** and `LENGTH(cipher)` equals the encoded length. Reconstruct the zigzag slot pattern for that length, count how many characters belong on each rail, split `cipher` into those contiguous segments in row order, then read characters back in zigzag visit order to recover the string before Rail Fence encoding.

---

### ALGORITHM: REVERSE(s)

Returns the characters of `s` in reverse order.

---

### Mapping to the Python program

| Concept | In pseudocode | In [`substitution_vigenere_cipher.py`](substitution_vigenere_cipher.py) |
|--------|----------------|----------------------------------------------------------------------|
| Full encrypt | ENCRYPT(P, K, r) | `hybrid_encrypt(plaintext, key, rails=r)` |
| Full decrypt | DECRYPT(C, K, r) | `hybrid_decrypt(ciphertext, key, rails=r)` |
| Rail row count | `r` | Parameter name **`rails`** (must be ≥ 2; errors say **“Numeric key…”** in user-facing paths) |

Menu flow: ask for text → **keyword** (`K`) → **numeric key for the extra layer** (this is **`r` / `rails`**; Enter uses default **3**). Decrypt asks for the **same keyword** and **same numeric key**. Only two lines are printed: **`Encryption:`** … and **`Decryption:`** ….

---

### ALGORITHM: MODULAR_INVERSE(a, m)

```
1. for i ← 1 to m − 1 do
2.     if (a · i) mod m = 1 then
3.         return i
4.     end if
5. end for
6. error "No modular inverse exists"
```

---

### UTILITY DEFINITIONS

| Utility | Meaning |
|---------|---------|
| REMOVE_SPACES(s) | removes all space characters |
| TO_UPPERCASE(s) | converts letters to uppercase |
| FILTER_LETTERS(s) | keeps only A–Z characters |
| ORD(c) | ASCII value of character |
| CHAR(x) | character from ASCII value |
| LENGTH(s) | number of characters |
