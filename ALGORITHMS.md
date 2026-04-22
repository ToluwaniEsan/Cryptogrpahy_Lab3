# CPT Cipher — Algorithm Specification

## Algorithm: Encrypt(P, K, r)

```
1.  clean ← TO_UPPERCASE(REMOVE_SPACES(P))
2.  n ← LENGTH(clean)

    // --- Affine Setup ---
3.  candidates ← (1,3,5,7,9,11,15,17,19,21,23,25)
4.  a ← candidates[n mod 12]
5.  b ← n mod 26

    // --- Step 1: Affine Transformation ---
6.  T ← empty string
7.  for each c in clean do
8.      if c is a letter then
9.          x ← ORD(c) − ORD('A')
10.         y ← (a·x + b) mod 26
11.         append CHAR(y + ORD('A')) to T
12.     else
13.         append c to T

    // --- Step 2: Vigenère ---
14. key ← TO_UPPERCASE(FILTER_LETTERS(K))
15. key_index ← 0
16. S ← empty string

17. for each c in T do
18.     if c is a letter then
19.         p ← ORD(c) − ORD('A')
20.         k ← ORD(key[key_index mod LENGTH(key)]) − ORD('A')
21.         append CHAR((p + k) mod 26 + ORD('A')) to S
22.         key_index ← key_index + 1
23.     else
24.         append c to S

    // --- Step 3: Rail Fence (Integrated) ---
25. rows[0…r−1] ← empty
26. rail ← 0, dir_down ← true

27. for each ch in S do
28.     append ch to rows[rail]
29.     if rail = 0 → dir_down ← true
30.     else if rail = r−1 → dir_down ← false
31.     rail ← rail + 1 if dir_down else rail − 1

32. R ← concatenate all rows

    // --- Step 4: Reverse ---
33. C ← REVERSE(R)

34. return C
```

---

## Algorithm: Decrypt(C, K, r)

```
1.  R ← REVERSE(C)
2.  n ← LENGTH(R)

    // --- Step 1: Rail Fence Decode (Integrated) ---
3.  pattern[0…n−1]
4.  rail ← 0, dir_down ← true

5.  for i = 0 → n−1 do
6.      pattern[i] ← rail
7.      if rail = 0 → dir_down ← true
8.      else if rail = r−1 → dir_down ← false
9.      rail ← rail + 1 if dir_down else rail − 1

10. count rails
11. split R into segments per rail
12. reconstruct S using pattern

    // --- Step 2: Vigenère Decode ---
13. key ← TO_UPPERCASE(FILTER_LETTERS(K))
14. key_index ← 0
15. T ← empty string

16. for each c in S do
17.     if c is letter then
18.         q ← ORD(c) − ORD('A')
19.         k ← ORD(key[key_index mod LENGTH(key)]) − ORD('A')
20.         append CHAR((q − k) mod 26 + ORD('A')) to T
21.         key_index ← key_index + 1
22.     else
23.         append c to T

    // --- Step 3: Affine Inverse ---
24. candidates ← (1,3,5,7,9,11,15,17,19,21,23,25)
25. a ← candidates[n mod 12]
26. b ← n mod 26
27. a_inv ← MODULAR_INVERSE(a, 26)

28. P ← empty string
29. for each c in T do
30.     if c is letter then
31.         y ← ORD(c) − ORD('A')
32.         x ← (a_inv · (y − b)) mod 26
33.         append CHAR(x + ORD('A')) to P
34.     else
35.         append c to P

36. return P
```
