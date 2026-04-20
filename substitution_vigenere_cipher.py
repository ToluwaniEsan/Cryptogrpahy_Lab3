"""CPT Cipher — Cascade Polyalphabetic Transposition: affine substitution, Vigenere, Rail Fence, then reverse."""

from __future__ import annotations


def _as_latin_upper_letter(char: str) -> str | None:
    """Return A–Z uppercase if char is a single Latin letter; else None."""
    if len(char) != 1:
        return None
    upper = char.upper()
    if len(upper) != 1:
        return None
    if "A" <= upper <= "Z":
        return upper
    return None


def _safe_multiplier(n: int) -> int:
    """Return a multiplier always invertible modulo 26 (coprime with 26)."""
    candidates = (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)
    return candidates[n % len(candidates)]


def _mod_inverse(a: int, m: int = 26) -> int:
    """Modular inverse of a under modulus m (m small; brute force is fine)."""
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    raise ValueError(f"No modular inverse for {a} modulo {m}")


def _substitution_on_clean(clean_text: str) -> str:
    """
    Affine map on Z/26Z: y = (a*x + b) mod 26, with x,y in 0..25.
    a depends on message length n and is always a unit mod 26; b = n mod 26.
    """
    n = len(clean_text)
    a = _safe_multiplier(n)
    b = n % 26
    out: list[str] = []
    for char in clean_text:
        u = _as_latin_upper_letter(char)
        if u is not None:
            x = ord(u) - 65
            y = (a * x + b) % 26
            out.append(chr(y + 65))
        else:
            out.append(char)
    return "".join(out)


def _substitution_inverse_on_clean(clean_text: str) -> str:
    """Inverse affine map using the same n-derived a and b as forward substitution."""
    n = len(clean_text)
    a = _safe_multiplier(n)
    b = n % 26
    a_inv = _mod_inverse(a)
    out: list[str] = []
    for char in clean_text:
        u = _as_latin_upper_letter(char)
        if u is not None:
            y = ord(u) - 65
            x = (a_inv * (y - b)) % 26
            out.append(chr(x + 65))
        else:
            out.append(char)
    return "".join(out)


def custom_substitution_cipher(text: str) -> str:
    """Strip spaces, then substitute A–Z letters; other characters pass through unchanged."""
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    return _substitution_on_clean(text.replace(" ", ""))


def _sanitized_vigenere_key(key: str) -> str:
    if not isinstance(key, str):
        raise TypeError("key must be a str")
    letters = "".join(ch.upper() for ch in key if _as_latin_upper_letter(ch) is not None)
    if not letters:
        raise ValueError("Vigenere key must contain at least one A-Z letter.")
    return letters


def _vigenere_apply(text: str, key_letters: str) -> str:
    """Vigenere encrypt using a pre-sanitized uppercase A-Z key (non-empty)."""
    key_len = len(key_letters)
    out: list[str] = []
    key_index = 0
    for char in text:
        u = _as_latin_upper_letter(char)
        if u is not None:
            shift = ord(key_letters[key_index % key_len]) - 65
            new_ord = (ord(u) - 65 + shift) % 26 + 65
            out.append(chr(new_ord))
            key_index += 1
        else:
            out.append(char)
    return "".join(out)


def _vigenere_decrypt(text: str, key_letters: str) -> str:
    """Vigenere decrypt; key stepping matches _vigenere_apply."""
    key_len = len(key_letters)
    out: list[str] = []
    key_index = 0
    for char in text:
        u = _as_latin_upper_letter(char)
        if u is not None:
            shift = ord(key_letters[key_index % key_len]) - 65
            new_ord = (ord(u) - 65 - shift) % 26 + 65
            out.append(chr(new_ord))
            key_index += 1
        else:
            out.append(char)
    return "".join(out)


def vigenere_encrypt(text: str, key: str) -> str:
    """Vigenere encryption; key letters only (non-letters in key ignored)."""
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    return _vigenere_apply(text, _sanitized_vigenere_key(key))


def vigenere_decrypt(text: str, key: str) -> str:
    """Vigenere decryption; key letters only (non-letters in key ignored)."""
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    return _vigenere_decrypt(text, _sanitized_vigenere_key(key))


def _rail_pattern_indices(length: int, rails: int) -> list[int]:
    """Rail index for each position in a zigzag of given length."""
    pattern: list[int] = []
    rail = 0
    dir_down = True
    for _ in range(length):
        pattern.append(rail)
        if rail == 0:
            dir_down = True
        elif rail == rails - 1:
            dir_down = False
        rail += 1 if dir_down else -1
    return pattern


def _rail_fence_encode(text: str, rails: int) -> str:
    """Rail Fence transposition: zigzag write, read rows top to bottom."""
    if rails < 2:
        raise ValueError("Numeric key must be at least 2.")
    if not text:
        return ""
    rows: list[list[str]] = [[] for _ in range(rails)]
    rail = 0
    dir_down = True
    for ch in text:
        rows[rail].append(ch)
        if rail == 0:
            dir_down = True
        elif rail == rails - 1:
            dir_down = False
        rail += 1 if dir_down else -1
    return "".join("".join(row) for row in rows)


def _rail_fence_decode(cipher: str, rails: int) -> str:
    """Inverse of _rail_fence_encode with the same rails and length."""
    if rails < 2:
        raise ValueError("Numeric key must be at least 2.")
    if not cipher:
        return ""
    n = len(cipher)
    pattern = _rail_pattern_indices(n, rails)
    counts = [0] * rails
    for p in pattern:
        counts[p] += 1
    chunks: list[list[str]] = []
    idx = 0
    for c in counts:
        chunks.append(list(cipher[idx : idx + c]))
        idx += c
    ptrs = [0] * rails
    out: list[str] = []
    for r in pattern:
        out.append(chunks[r][ptrs[r]])
        ptrs[r] += 1
    return "".join(out)


def _reverse_layer(s: str) -> str:
    """Full string reversal (permutation layer)."""
    return s[::-1]


def hybrid_encrypt(plaintext: str, key: str, rails: int = 3) -> str:
    """
    Full encrypt: affine substitution -> Vigenere -> Rail Fence -> reverse.
    spaces removed at the start; decrypt recovers space-free plaintext.
    """
    if not isinstance(plaintext, str):
        raise TypeError("plaintext must be a str")
    if rails < 2:
        raise ValueError("Numeric key must be at least 2.")
    after_sub_vig = vigenere_encrypt(custom_substitution_cipher(plaintext), key)
    fenced = _rail_fence_encode(after_sub_vig, rails)
    return _reverse_layer(fenced)


def hybrid_decrypt(ciphertext: str, key: str, rails: int = 3) -> str:
    """Full decrypt: un-reverse -> Rail Fence decode -> Vigenere decrypt -> inverse affine."""
    if not isinstance(ciphertext, str):
        raise TypeError("ciphertext must be a str")
    if rails < 2:
        raise ValueError("Numeric key must be at least 2.")
    unrev = _reverse_layer(ciphertext)
    after_rail = _rail_fence_decode(unrev, rails)
    after_vig = vigenere_decrypt(after_rail, key)
    return _substitution_inverse_on_clean(after_vig)


def combined_hybrid_encrypt(text: str, key: str, rails: int = 3) -> str:
    """
    Same as hybrid_encrypt without calling vigenere_encrypt: inlines _vigenere_apply.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if rails < 2:
        raise ValueError("Numeric key must be at least 2.")
    key_letters = _sanitized_vigenere_key(key)
    s = _substitution_on_clean(text.replace(" ", ""))
    s = _vigenere_apply(s, key_letters)
    s = _rail_fence_encode(s, rails)
    return _reverse_layer(s)


def combined_hybrid_decrypt(ciphertext: str, key: str, rails: int = 3) -> str:
    """
    Same as hybrid_decrypt without calling vigenere_decrypt; uses _vigenere_decrypt.
    """
    if not isinstance(ciphertext, str):
        raise TypeError("ciphertext must be a str")
    if rails < 2:
        raise ValueError("Numeric key must be at least 2.")
    key_letters = _sanitized_vigenere_key(key)
    s = _reverse_layer(ciphertext)
    s = _rail_fence_decode(s, rails)
    s = _vigenere_decrypt(s, key_letters)
    return _substitution_inverse_on_clean(s)


def _self_check_round_trip() -> None:
    plain, k = "Hello World", "KEY"
    rails = 3
    clean = plain.replace(" ", "")
    c = hybrid_encrypt(plain, k, rails)
    d1 = hybrid_decrypt(c, k, rails)
    d2 = combined_hybrid_decrypt(c, k, rails)
    expected = "".join(ch.upper() if _as_latin_upper_letter(ch) is not None else ch for ch in clean)
    assert d1 == d2 == expected
    assert c == combined_hybrid_encrypt(plain, k, rails)
    assert vigenere_decrypt(vigenere_encrypt("ABC", k), k) == "ABC"
    # rail round-trip without other layers
    rf = _rail_fence_encode("abcdefghij", 3)
    assert _rail_fence_decode(rf, 3) == "abcdefghij"


def _parse_rails_input(raw: str, default: int = 3) -> int:
    raw = raw.strip()
    if not raw:
        return default
    r = int(raw)
    if r < 2:
        raise ValueError("Numeric key must be a whole number >= 2.")
    return r


def _run_menu() -> None:
    print("CPT Cipher — encrypt or decrypt messages below.")
    while True:
        print()
        print("  1 = Encrypt")
        print("  2 = Decrypt")
        print("  3 = Exit")
        choice = input("Choose (1 / 2 / 3): ").strip().lower()

        if choice in ("3", "exit", "q", "quit"):
            print("Goodbye.")
            break

        if choice in ("1", "encrypt", "e"):
            try:
                word = input("Enter a word or phrase to encrypt: ").strip()
                key = input("Keyword (letters only count; non-letters ignored): ").strip()
                rails_in = input(
                    "Numeric key for the extra layer (whole number ≥ 2, Enter = 3): "
                ).strip()
                rails = _parse_rails_input(rails_in, 3)
                ciphertext = hybrid_encrypt(word, key, rails)
                print(f"Encryption: '{ciphertext}'")
            except (TypeError, ValueError) as e:
                print(f"Error: {e}")

        elif choice in ("2", "decrypt", "d"):
            try:
                cipher = input("Enter ciphertext to decrypt: ").strip()
                key = input("Same keyword as when you encrypted: ").strip()
                rails_in = input(
                    "Same numeric key as when you encrypted (Enter = 3): "
                ).strip()
                rails = _parse_rails_input(rails_in, 3)
                plain = hybrid_decrypt(cipher, key, rails)
                print(f"Decryption: '{plain}'")
            except (TypeError, ValueError) as e:
                print(f"Error: {e}")

        else:
            print("Invalid choice. Enter 1, 2, or 3.")


if __name__ == "__main__":
    _self_check_round_trip()
    _run_menu()
