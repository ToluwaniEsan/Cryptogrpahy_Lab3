"""RSA Encryption and Decryption Demo with 'Go Bulldogs.'
Reference: Rivest, R., Shamir, A., & Adleman, L. (1978)."""

from rsa import RSA


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
