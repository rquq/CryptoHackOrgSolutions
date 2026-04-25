from Crypto.Cipher import AES

key = b'sixteen_byte_key'
plaintext = b'crypto_is_fun_!!'

cipher = AES.new(key, AES.MODE_ECB)

ciphertext = cipher.encrypt(plaintext)
print(f"Ciphertext (Hex): {ciphertext.hex()}")

decrypted_block = cipher.decrypt(ciphertext)
print(f"Decrypted (Text): {decrypted_block.decode()}")

assert plaintext == decrypted_block