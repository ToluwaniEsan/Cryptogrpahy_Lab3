# Hybrid Substitution–Vigenère Cipher (Algorithm Specification)

### ALGORITHM: ENCRYPT(P, K)

```
1.  clean ← REMOVE_SPACES(P)
2.  clean ← TO_UPPERCASE(clean)
3.  n ← LENGTH(clean)
4.  candidates ← (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)
5.  a ← candidates[n mod 12]
6.  b ← n mod 26
7.  S ← empty string
8.  for each character c in clean do
9.      if c ∈ {A, …, Z} then
10.         x ← ORD(c) − ORD('A')
11.         y ← (a·x + b) mod 26
12.         S ← S + CHAR(y + ORD('A'))
13.     else
14.         S ← S + c
15.     end if
16. end for
17. key_letters ← FILTER_LETTERS(K)
18. key_letters ← TO_UPPERCASE(key_letters)
19. key_len ← LENGTH(key_letters)
20. key_index ← 0
21. C ← empty string
22. for each character c in S do
23.     if c ∈ {A, …, Z} then
24.         p ← ORD(c) − ORD('A')
25.         k ← ORD(key_letters[key_index mod key_len]) − ORD('A')
26.         cipher_index ← (p + k) mod 26
27.         C ← C + CHAR(cipher_index + ORD('A'))
28.         key_index ← key_index + 1
29.     else
30.         C ← C + c
31.     end if
32. end for
33. return C
```

### ALGORITHM: DECRYPT(C, K)

```
1.  n ← LENGTH(C)
2.  key_letters ← FILTER_LETTERS(K)
3.  key_letters ← TO_UPPERCASE(key_letters)
4.  key_len ← LENGTH(key_letters)
5.  key_index ← 0
6.  S ← empty string
7.  for each character c in C do
8.      if c ∈ {A, …, Z} then
9.          q ← ORD(c) − ORD('A')
10.         k ← ORD(key_letters[key_index mod key_len]) − ORD('A')
11.         plain_index ← (q − k) mod 26
12.         S ← S + CHAR(plain_index + ORD('A'))
13.         key_index ← key_index + 1
14.     else
15.         S ← S + c
16.     end if
17. end for
18. candidates ← (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)
19. a ← candidates[n mod 12]
20. b ← n mod 26
21. a_inv ← MODULAR_INVERSE(a, 26)
22. P′ ← empty string
23. for each character c in S do
24.     if c ∈ {A, …, Z} then
25.         y ← ORD(c) − ORD('A')
26.         x ← (a_inv · (y − b)) mod 26
27.         P′ ← P′ + CHAR(x + ORD('A'))
28.     else
29.         P′ ← P′ + c
30.     end if
31. end for
32. return P′
```

### ALGORITHM: MODULAR_INVERSE(a, m)

```
1. for i ← 1 to m − 1 do
2.     if (a · i) mod m = 1 then
3.         return i
4.     end if
5. end for
6. error "No modular inverse exists"
```

### UTILITY DEFINITIONS

| Utility | Meaning |
|---------|---------|
| REMOVE_SPACES(s) | removes all space characters |
| TO_UPPERCASE(s) | converts letters to uppercase |
| FILTER_LETTERS(s) | keeps only A–Z characters |
| ORD(c) | ASCII value of character |
| CHAR(x) | character from ASCII value |
| LENGTH(s) | number of characters |
