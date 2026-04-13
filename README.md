# Cryptography Lab 3: RSA Algorithm Implementation

## Overview

This project implements the **RSA (Rivest–Shamir–Adleman)** cryptographic algorithm in Python. RSA is one of the most widely used asymmetric encryption algorithms that enables secure communication and digital signatures.

## Features

- **Key Generation**: Generates large prime numbers and derives RSA public/private key pairs
- **Encryption**: Encrypts messages using the public key
- **Decryption**: Decrypts messages using the private key
- **Primality Testing**: Uses Miller-Rabin probabilistic primality test
- **Modular Arithmetic**: Implements extended Euclidean algorithm for modular inverse calculation
- **Detailed Documentation**: Fully commented code with academic references

## Files

- **rsa.py**: Core RSA implementation with all cryptographic operations
- **demo.py**: Demonstration script showing encryption/decryption of "Go Bulldogs."
- **README.md**: This file

## Mathematical Background

### RSA Key Generation

1. Generate two large distinct prime numbers: **p** and **q**
2. Calculate the modulus: **n = p × q**
3. Calculate Euler's totient: **φ(n) = (p-1) × (q-1)**
4. Choose public exponent **e** such that:
   - 1 < e < φ(n)
   - gcd(e, φ(n)) = 1
   - Typically e = 65537
5. Calculate private exponent **d** such that:
   - (e × d) ≡ 1 (mod φ(n))
   - d is calculated using the Extended Euclidean Algorithm

**Public Key**: (e, n)
**Private Key**: (d, n)

### Encryption

For plaintext message **m**, the ciphertext **c** is calculated as:

**c ≡ m^e (mod n)**

Each character is converted to its ASCII value and encrypted individually.

### Decryption

For ciphertext **c**, the plaintext **m** is recovered as:

**m ≡ c^d (mod n)**

## Demo: "Go Bulldogs."

### Running the Demonstration

```bash
python demo.py
```

This script will:
1. Generate a new RSA key pair
2. Display the public and private keys
3. Encrypt the message "Go Bulldogs."
4. Show the encrypted values
5. Decrypt back to the original message
6. Verify the decryption is correct

### Expected Output Structure

```
Step 1: Initialize RSA
Step 2: Generate Key Pairs
  Public Key (e, n): (65537, [large number])
  Private Key (d, n): ([large number], [large number])

Step 3: Original Message
  "Go Bulldogs."

Step 4: Encryption
  Encrypted values: [encrypted numbers]

Step 5: Decryption
  Decrypted Message: "Go Bulldogs."

Step 6: Verification
  ✓ SUCCESS: Messages match!
```

## Security Considerations

This implementation is **for educational purposes only**. Key security notes:

1. **Key Size**: Uses 128-bit keys for demonstration. Production systems should use:
   - Minimum: 2048-bit RSA keys
   - Recommended: 4096-bit RSA keys

2. **Character Limitation**: This implementation encrypts each character individually. Large numbers greater than the modulus cannot be encrypted directly without padding schemes.

3. **Padding**: Real-world implementations use padding schemes like:
   - PKCS#1 v1.5
   - Optimal Asymmetric Encryption Padding (OAEP)
   - ISO/IEC 9796

4. **Random Number Generation**: Uses Python's `random.getrandbits()`. For cryptographic applications, use `secrets` or `os.urandom()`.

5. **Timing Attacks**: The simple modular exponentiation is vulnerable to timing attacks. Use constant-time implementations in production.

## References

1. **Original RSA Paper**:
   - Rivest, R., Shamir, A., & Adleman, L. (1978). "A method for obtaining digital signatures and public-key cryptosystems." Communications of the ACM, 21(2), 120-126.

2. **Standards**:
   - RFC 3447: PKCS #1: RSA Cryptography Specifications Version 2.1
   - NIST Special Publication 800-2: Number Theory: Number Theoretic Functions

3. **Academic References**:
   - Menezes, A. J., van Oorschot, P. C., & Vanstone, S. A. (1996). "Handbook of Applied Cryptography." CRC Press.
   - Knuth, D. E. (1997). "The Art of Computer Programming, Volume 2: Seminumerical Algorithms."

4. **Algorithms**:
   - Miller-Rabin Primality Test: Miller, G. L., & Rabin, M. O. (1976). "Probabilistic algorithm for testing primality." Journal of Computer and System Sciences, 13(3), 300-317.
   - Extended Euclidean Algorithm: Ancient mathematical algorithm, documented in Knuth (above)
   - Modular Exponentiation: Binary exponentiation method for efficient computation

## Implementation Details

### Prime Generation
- Uses Miller-Rabin primality test with k=40 rounds for high confidence
- Generates random numbers with specified bit length
- Ensures numbers are odd and have correct bit length

### Modular Arithmetic
- Extended Euclidean Algorithm finds modular inverse
- Binary exponentiation for efficient modular exponentiation
- Python's `pow(base, exp, mod)` for optimized computation

### Key Generation Process
```
1. Generate prime p (128-bit)
2. Generate prime q (128-bit, q ≠ p)
3. Calculate n = p × q
4. Calculate φ(n) = (p-1) × (q-1)
5. Choose e = 65537 (or smaller if necessary)
6. Calculate d = e^(-1) mod φ(n)
7. Return public_key = (e, n), private_key = (d, n)
```

## Usage Example

```python
from rsa import RSA

# Initialize RSA with 128-bit key size
rsa = RSA(key_size=128)

# Generate key pairs
public_key, private_key = rsa.generate_keys()

# Message to encrypt
message = "Go Bulldogs."

# Encrypt
ciphertext = rsa.encrypt(message)
print(f"Encrypted: {ciphertext}")

# Decrypt
plaintext = rsa.decrypt(ciphertext)
print(f"Decrypted: {plaintext}")
```

## Performance Metrics

For a 128-bit key size:
- Key generation time: ~1-2 seconds
- Encryption time: ~milliseconds per character
- Decryption time: ~milliseconds per character

**Note**: Increase key size for production use. Larger keys provide better security but slower execution.

## Future Enhancements

1. Implement OAEP padding scheme
2. Support variable-length message encryption
3. Add digital signature support
4. Optimize using CRT (Chinese Remainder Theorem)
5. Implement constant-time operations for timing attack resistance
6. Add support for larger numbers using Python's unlimited precision
7. Performance benchmarking and optimization

## Author

Cryptography Lab 3 - April 2026

## License

Educational Use Only
