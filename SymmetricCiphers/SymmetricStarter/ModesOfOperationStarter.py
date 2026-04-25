import requests

url = "https://aes.cryptohack.org/block_cipher_starter"
c = requests.get(f"{url}/encrypt_flag").json()["ciphertext"]
p = requests.get(f"{url}/decrypt/{c}").json()["plaintext"]

print(bytes.fromhex(p).decode())