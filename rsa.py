"""RSA Encryption and Decryption Demo with 'Go Bulldogs.'

References:
- Rivest, R., Shamir, A., & Adleman, L. (1978). A method for obtaining digital
  signatures and public-key cryptosystems. Communications of the ACM, 21(2), 120-126.
- Miller, G. L., & Rabin, M. O. (1976). Probabilistic algorithm for testing primality.
"""

import random
from typing import Tuple


class RSA:
    """RSA encryption/decryption with public key (e,n) and private key (d,n)."""

    def __init__(self, key_size: int = 128):
        """Initialize RSA with key_size in bits (default 128)."""
        self.key_size = key_size
        self.public_key = None
        self.private_key = None

    @staticmethod
    def is_prime(n: int, k: int = 40) -> bool:
        """Miller-Rabin primality test. Returns True if n is probably prime."""
        if n < 2:
            return False
        if n in (2, 3):
            return True
        if n % 2 == 0:
            return False

        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        for _ in range(k):
            a = random.randrange(2, n - 1)
            x = pow(a, d, n)
            if x in (1, n - 1):
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    def generate_prime(self) -> int:
        """Generate a random prime number of key_size bits."""
        while True:
            num = random.getrandbits(self.key_size)
            num |= (1 << (self.key_size - 1))
            num |= 1
            if self.is_prime(num):
                return num

    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Calculate GCD using Euclidean algorithm."""
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        """Return (gcd, x, y) where a*x + b*y = gcd."""
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = RSA.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    @staticmethod
    def mod_inverse(e: int, phi: int) -> int:
        """Calculate d where (e * d) mod phi = 1."""
        gcd, x, _ = RSA.extended_gcd(e, phi)
        if gcd != 1:
            raise ValueError("Modular inverse does not exist")
        return x % phi

    def _find_suitable_e(self, phi: int) -> int:
        """Find suitable public exponent e if 65537 is too large for phi."""
        for e in (65537, 17, 7, 5, 3):
            if e < phi and self.gcd(e, phi) == 1:
                return e
        e = 3
        while self.gcd(e, phi) != 1:
            e += 2
        return e

    def generate_keys(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Generate RSA key pairs. Returns (public_key, private_key)."""
        p = self.generate_prime()
        q = self.generate_prime()
        while p == q:
            q = self.generate_prime()

        n = p * q
        phi = (p - 1) * (q - 1)
        e = 65537 if 65537 < phi else self._find_suitable_e(phi)
        d = self.mod_inverse(e, phi)

        self.public_key = (e, n)
        self.private_key = (d, n)
        return self.public_key, self.private_key

    def encrypt(self, plaintext: str, public_key: Tuple[int, int] = None) -> list:
        """Encrypt plaintext using c = m^e mod n for each character."""
        if public_key is None:
            public_key = self.public_key
        if public_key is None:
            raise ValueError("Public key not available. Generate keys first.")

        e, n = public_key
        return [pow(ord(char), e, n) for char in plaintext]

    def decrypt(self, ciphertext: list, private_key: Tuple[int, int] = None) -> str:
        """Decrypt ciphertext using m = c^d mod n for each value."""
        if private_key is None:
            private_key = self.private_key
        if private_key is None:
            raise ValueError("Private key not available. Generate keys first.")

        d, n = private_key
        return "".join(chr(pow(value, d, n)) for value in ciphertext)

    def display_keys(self) -> None:
        """Display current public and private keys."""
        if self.public_key:
            e, n = self.public_key
            print("Public Key (e, n):")
            print(f"  e (exponent): {e}")
            print(f"  n (modulus): {n}")
        if self.private_key:
            d, n = self.private_key
            print("\nPrivate Key (d, n):")
            print(f"  d (exponent): {d}")
            print(f"  n (modulus): {n}")


def main():
    """Interactive RSA encryption/decryption."""
    
    # Initialize RSA and generate keys once
    rsa = RSA(key_size=128)
    rsa.generate_keys()
    
    print("RSA ENCRYPTION AND DECRYPTION")
    print("-" * 50)
    rsa.display_keys()
    print()
    
    while True:
        print("\nOptions:")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            plaintext = input("Enter message to encrypt: ")
            ciphertext = rsa.encrypt(plaintext)
            print(f"\nEncrypted: {ciphertext}")
        
        elif choice == "2":
            try:
                ciphertext_input = input("Enter encrypted values (comma-separated): ")
                ciphertext = [int(x.strip()) for x in ciphertext_input.split(",")]
                decrypted = rsa.decrypt(ciphertext)
                print(f"\nDecrypted: {decrypted}")
            except ValueError:
                print("Invalid input. Please enter numbers separated by commas.")
        
        elif choice == "3":
            print("Exiting...")
            break
        
        else:
            print("Invalid option. Please select 1-3.")


if __name__ == "__main__":
    main()
