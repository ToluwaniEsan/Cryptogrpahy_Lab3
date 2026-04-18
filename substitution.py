def custom_substitution_cipher(text):
    clean_text = text.replace(" ", "")
    
    word_length = len(clean_text)
    
    encrypted_text = ""
    
    for char in clean_text:
        if char.isalpha():
            char_upper = char.upper()
            
            letter_val = ord(char_upper) - 64 
            
            new_val = ((letter_val * word_length - 1) % 26) + 1
            
            encrypted_text += chr(new_val + 64)
        else:
            encrypted_text += char
            
    return encrypted_text

word = input("Enter a word or phrase to encrypt: ")
encrypted_string = custom_substitution_cipher(word)

print(f"Original: '{word}'")
print(f"Length (no spaces): {len(word.replace(' ', ''))}")
print(f"Encrypted: '{encrypted_string}'")