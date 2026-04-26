from pwn import *
import json
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def decrypt_flag(shared_secret, iv, ciphertext):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode())
    key = sha1.digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv))
    return unpad(cipher.decrypt(bytes.fromhex(ciphertext)), 16).decode()


r = remote('socket.cryptohack.org', 13380)


r.recvuntil(b"Intercepted from Alice: ")
data = json.loads(r.recvline().decode())


p = int(data['p'], 16)
g = int(data['g'], 16)
A = int(data['A'], 16)


r.recvuntil(b"Intercepted from Bob: ")
B = int(json.loads(r.recvline().decode())['B'], 16)


r.recvuntil(b"Intercepted from Alice: ")
encrypted = json.loads(r.recvline().decode())


# Solve for secret 'a' using modular inverse in additive group
# g * a = A (mod p) => a = A * inv(g) (mod p)
a = (A * pow(g, -1, p)) % p
shared_secret = (B * a) % p


print(decrypt_flag(shared_secret, encrypted['iv'], encrypted['encrypted_flag']))
