from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import requests, json

BASE_URL = "https://aes.cryptohack.org/oracular_spectacular"

def encrypt(plaintext_hex):
    r = requests.get(f"{BASE_URL}/encrypt/{plaintext_hex}/")
    return r.json()

def decrypt_oracle(ciphertext_hex):
    """Returns True if padding is valid"""
    r = requests.get(f"{BASE_URL}/decrypt/{ciphertext_hex}/")
    resp = r.json()
    return "error" not in resp  # valid padding = no error

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def attack_block(c1, c2):
    """Decrypt c2 using c1 as the IV via padding oracle"""
    intermediate = bytearray(16)
    
    for i in range(15, -1, -1):
        pad_byte = 16 - i
        crafted_c1 = bytearray(16)
        
        # Fix known bytes
        for j in range(i + 1, 16):
            crafted_c1[j] = intermediate[j] ^ pad_byte
        
        for guess in range(256):
            crafted_c1[i] = guess
            ct_hex = (bytes(crafted_c1) + c2).hex()
            
            if decrypt_oracle(ct_hex):
                intermediate[i] = guess ^ pad_byte
                break
    
    return xor_bytes(intermediate, c1)

def full_attack(ciphertext_hex):
    ct = bytes.fromhex(ciphertext_hex)
    iv = ct[:16]
    blocks = [ct[i:i+16] for i in range(16, len(ct), 16)]
    
    plaintext = b""
    prev = iv
    for block in blocks:
        pt_block = attack_block(prev, block)
        plaintext += pt_block
        prev = block
    
    return unpad(plaintext, 16)

# Run the attack
enc = encrypt(b"".hex())  # get a fresh ciphertext
ct_hex = enc["ciphertext"]
flag = full_attack(ct_hex)
print(flag.decode())