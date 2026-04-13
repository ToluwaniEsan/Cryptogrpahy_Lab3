"""
RSA Encryption and Decryption Demonstration

This script demonstrates the RSA algorithm by:
1. Generating RSA key pairs
2. Encrypting the plaintext message "Go Bulldogs."
3. Decrypting the ciphertext back to the original message

References:
- Rivest, R., Shamir, A., & Adleman, L. (1978). A method for obtaining digital
  signatures and public-key cryptosystems. Communications of the ACM, 21(2), 120-126.

Author: Cryptography Lab 3
Date: April 2026
"""

from rsa import RSA


def main():
    """Run RSA encryption and decryption demonstration."""
    
    print("="*70)
    print("RSA ENCRYPTION AND DECRYPTION DEMONSTRATION")
    print("="*70)
    print()
    
    # Initialize RSA with 128-bit key size for demonstration
    # Note: In production, use larger key sizes (2048-bit or 4096-bit)
    print("Step 1: Initializing RSA with 128-bit key size")
    print("-" * 70)
    rsa = RSA(key_size=128)
    print("RSA instance created with 128-bit key size")
    print()
    
    # Generate public and private key pairs
    print("Step 2: Generating RSA Key Pairs")
    print("-" * 70)
    print("Generating two large prime numbers and deriving key pairs...")
    public_key, private_key = rsa.generate_keys()
    rsa.display_keys()
    print()
    
    # Define the plaintext message
    plaintext = "Go Bulldogs."
    print("Step 3: Plaintext Message")
    print("-" * 70)
    print(f"Original Message: \"{plaintext}\"")
    print(f"Message Length: {len(plaintext)} characters")
    print()
    
    # Display character breakdown
    print("Character Breakdown (ASCII values):")
    for i, char in enumerate(plaintext):
        print(f"  {i+1:2d}. '{char}' → ASCII {ord(char)}")
    print()
    
    # Encrypt the plaintext
    print("Step 4: Encryption Process")
    print("-" * 70)
    print("Applying RSA encryption: ciphertext = plaintext^e mod n")
    ciphertext = rsa.encrypt(plaintext)
    print(f"Encrypted values: {ciphertext}")
    print()
    
    # Display encryption details
    print("Encryption Details (for each character):")
    e, n = public_key
    for i, char in enumerate(plaintext):
        plaintext_val = ord(char)
        ciphertext_val = ciphertext[i]
        print(f"  '{char}' → {plaintext_val}^{e} mod {n} = {ciphertext_val}")
    print()
    
    # Decrypt the ciphertext
    print("Step 5: Decryption Process")
    print("-" * 70)
    print("Applying RSA decryption: plaintext = ciphertext^d mod n")
    decrypted_message = rsa.decrypt(ciphertext)
    print(f"Decrypted Message: \"{decrypted_message}\"")
    print()
    
    # Display decryption details
    print("Decryption Details (for each character):")
    d, n = private_key
    for i, cipher_val in enumerate(ciphertext):
        decrypted_val = ord(decrypted_message[i])
        print(f"  {cipher_val}^{d} mod {n} = {decrypted_val} → '{decrypted_message[i]}'")
    print()
    
    # Verify correctness
    print("Step 6: Verification")
    print("-" * 70)
    if plaintext == decrypted_message:
        print("✓ SUCCESS: Decrypted message matches original plaintext!")
        print(f"  Original:  \"{plaintext}\"")
        print(f"  Decrypted: \"{decrypted_message}\"")
    else:
        print("✗ FAILURE: Messages do not match!")
        print(f"  Original:  \"{plaintext}\"")
        print(f"  Decrypted: \"{decrypted_message}\"")
    print()
    
    # Display security information
    print("Step 7: Security Information")
    print("-" * 70)
    e, n = public_key
    d, n = private_key
    bit_length = n.bit_length()
    print(f"Modulus (n) bit length: {bit_length} bits")
    print(f"Public Exponent (e): {e}")
    print(f"Private Exponent (d): {d}")
    print()
    print("Note: This demonstration uses a small key size (128-bit) for simplicity.")
    print("For production use, RSA should use at least 2048-bit keys.")
    print()
    
    print("="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
