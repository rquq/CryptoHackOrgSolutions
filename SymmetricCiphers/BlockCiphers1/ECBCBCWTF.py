import requests

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

r = requests.get("http://aes.cryptohack.org/ecbcbcwtf/encrypt_flag/")
ct = bytes.fromhex(r.json()["ciphertext"])

iv = ct[:16]
c1 = ct[16:32]
c2 = ct[32:]

r1 = requests.get(f"http://aes.cryptohack.org/ecbcbcwtf/decrypt/{c1.hex()}/")
p1_xor = bytes.fromhex(r1.json()["plaintext"])
p1 = xor(p1_xor, iv)

r2 = requests.get(f"http://aes.cryptohack.org/ecbcbcwtf/decrypt/{c2.hex()}/")
p2_xor = bytes.fromhex(r2.json()["plaintext"])
p2 = xor(p2_xor, c1)

print((p1 + p2).decode())