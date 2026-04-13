"""
RSA (Rivest–Shamir–Adleman) Encryption Algorithm Implementation

This module implements the RSA cryptographic algorithm for secure encryption
and decryption of messages.

References:
- Rivest, R., Shamir, A., & Adleman, L. (1978). A method for obtaining digital
  signatures and public-key cryptosystems. Communications of the ACM, 21(2), 120-126.
- NIST Special Publication 800-2: Number Theory: Number Theoretic Functions
- RFC 3447: PKCS #1: RSA Cryptography Specifications Version 2.1
- Handbook of Applied Cryptography: Chapter 2 - RSA Public-Key Cryptosystem
  http://www.cacr.math.uwaterloo.ca/hac/

Author: Cryptography Lab 3
Date: April 2026
"""

import random
from typing import Tuple


class RSA:
    """
    RSA Cryptography Implementation
    
    This class implements the RSA algorithm which uses a pair of keys:
    - Public Key (e, n): used for encryption
    - Private Key (d, n): used for decryption
    """
    
    def __init__(self, key_size: int = 128):
        """
        Initialize RSA with specified key size.
        
        Args:
            key_size: The size of the prime numbers (in bits). Default is 128.
        """
        self.key_size = key_size
        self.public_key = None
        self.private_key = None
    
    @staticmethod
    def is_prime(n: int, k: int = 40) -> bool:
        """
        Miller-Rabin primality test.
        
        Determines if a number is prime with probability of correctness
        at least 1 - 4^(-k).
        
        Reference: Miller, G. L., & Rabin, M. O. (1976). Probabilistic algorithm
        for testing primality. Journal of Computer and System Sciences, 13(3), 300-317.
        
        Args:
            n: The number to test for primality
            k: Number of rounds (higher k = higher confidence)
            
        Returns:
            bool: True if n is probably prime, False if definitely composite
        """
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        
        # Write n-1 as 2^r * d where d is odd
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        
        # Perform k rounds of testing
        for _ in range(k):
            a = random.randrange(2, n - 1)
            x = pow(a, d, n)
            
            if x == 1 or x == n - 1:
                continue
            
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        
        return True
    
    def generate_prime(self) -> int:
        """
        Generate a random prime number of specified key_size.
        
        Returns:
            int: A prime number suitable for RSA
        """
        while True:
            num = random.getrandbits(self.key_size)
            # Set the highest bit to 1 to ensure correct bit length
            num |= (1 << (self.key_size - 1))
            # Set the lowest bit to 1 to ensure it's odd
            num |= 1
            
            if self.is_prime(num):
                return num
    
    @staticmethod
    def gcd(a: int, b: int) -> int:
        """
        Calculate the Greatest Common Divisor using Euclidean algorithm.
        
        Reference: Euclid of Alexandria (circa 300 BC). Elements, Book VII.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            int: The GCD of a and b
        """
        while b:
            a, b = b, a % b
        return a
    
    @staticmethod
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        """
        Extended Euclidean Algorithm to find modular inverse.
        
        Returns tuple (gcd, x, y) such that a*x + b*y = gcd
        
        Reference: Knuth, D. E. (1997). The Art of Computer Programming,
        Volume 2: Seminumerical Algorithms, Third Edition.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Tuple[int, int, int]: (gcd, x, y) where a*x + b*y = gcd
        """
        if a == 0:
            return b, 0, 1
        
        gcd, x1, y1 = RSA.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        
        return gcd, x, y
    
    @staticmethod
    def mod_inverse(e: int, phi: int) -> int:
        """
        Calculate the modular multiplicative inverse of e mod phi.
        
        Finds d such that (e * d) mod phi = 1
        
        Args:
            e: The public exponent
            phi: Euler's totient function result
            
        Returns:
            int: The modular inverse d
            
        Raises:
            ValueError: If modular inverse does not exist
        """
        gcd, x, _ = RSA.extended_gcd(e, phi)
        
        if gcd != 1:
            raise ValueError("Modular inverse does not exist")
        
        return (x % phi + phi) % phi
    
    def generate_keys(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Generate RSA public and private key pairs.
        
        Process:
        1. Generate two large prime numbers p and q
        2. Calculate n = p * q
        3. Calculate φ(n) = (p-1)(q-1)
        4. Choose e such that 1 < e < φ(n) and gcd(e, φ(n)) = 1
        5. Calculate d using extended Euclidean algorithm
        
        Returns:
            Tuple[Tuple[int, int], Tuple[int, int]]: Public key (e, n), Private key (d, n)
        """
        # Generate two distinct prime numbers
        p = self.generate_prime()
        q = self.generate_prime()
        
        # Ensure p and q are different
        while p == q:
            q = self.generate_prime()
        
        # Calculate n = p * q
        n = p * q
        
        # Calculate Euler's totient function φ(n) = (p-1)(q-1)
        phi = (p - 1) * (q - 1)
        
        # Choose e (public exponent) - typically 65537
        # e must satisfy: 1 < e < φ(n) and gcd(e, φ(n)) = 1
        e = 65537
        
        # If e is too large, choose a smaller value
        if e >= phi:
            e = self._find_suitable_e(phi)
        
        # Calculate d (private exponent) using extended Euclidean algorithm
        d = self.mod_inverse(e, phi)
        
        # Store keys
        self.public_key = (e, n)
        self.private_key = (d, n)
        
        return self.public_key, self.private_key
    
    def _find_suitable_e(self, phi: int) -> int:
        """
        Find a suitable public exponent e if default (65537) is too large.
        
        Args:
            phi: Euler's totient function result
            
        Returns:
            int: A suitable public exponent
        """
        common_e_values = [65537, 17, 7, 5, 3]
        for e in common_e_values:
            if e < phi and self.gcd(e, phi) == 1:
                return e
        
        # Fallback: find next suitable odd number
        e = 3
        while self.gcd(e, phi) != 1:
            e += 2
        return e
    
    def encrypt(self, plaintext: str, public_key: Tuple[int, int] = None) -> list:
        """
        Encrypt plaintext using RSA public key.
        
        Process:
        1. Convert each character to its ASCII value
        2. Apply RSA encryption: ciphertext = (plaintext)^e mod n
        
        Args:
            plaintext: The message to encrypt
            public_key: Tuple of (e, n). If None, uses self.public_key
            
        Returns:
            list: List of encrypted character values
        """
        if public_key is None:
            public_key = self.public_key
        
        if public_key is None:
            raise ValueError("Public key not available. Generate keys first.")
        
        e, n = public_key
        encrypted_chars = []
        
        for char in plaintext:
            # Convert character to ASCII value
            plaintext_value = ord(char)
            
            # Encrypt using formula: c = m^e mod n
            ciphertext_value = pow(plaintext_value, e, n)
            encrypted_chars.append(ciphertext_value)
        
        return encrypted_chars
    
    def decrypt(self, ciphertext: list, private_key: Tuple[int, int] = None) -> str:
        """
        Decrypt ciphertext using RSA private key.
        
        Process:
        1. Apply RSA decryption: plaintext = (ciphertext)^d mod n
        2. Convert each decrypted value to its character representation
        
        Args:
            ciphertext: List of encrypted values
            private_key: Tuple of (d, n). If None, uses self.private_key
            
        Returns:
            str: The decrypted message
        """
        if private_key is None:
            private_key = self.private_key
        
        if private_key is None:
            raise ValueError("Private key not available. Generate keys first.")
        
        d, n = private_key
        decrypted_chars = []
        
        for ciphertext_value in ciphertext:
            # Decrypt using formula: m = c^d mod n
            plaintext_value = pow(ciphertext_value, d, n)
            
            # Convert ASCII value back to character
            decrypted_char = chr(plaintext_value)
            decrypted_chars.append(decrypted_char)
        
        return ''.join(decrypted_chars)
    
    def display_keys(self) -> None:
        """Display the current public and private keys."""
        if self.public_key:
            e, n = self.public_key
            print(f"Public Key (e, n):")
            print(f"  e (exponent): {e}")
            print(f"  n (modulus): {n}")
        
        if self.private_key:
            d, n = self.private_key
            print(f"\nPrivate Key (d, n):")
            print(f"  d (exponent): {d}")
            print(f"  n (modulus): {n}")
