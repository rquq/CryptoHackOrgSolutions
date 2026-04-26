from pwn import *
import json
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


r = remote('socket.cryptohack.org', 13373)


def decrypt_flag(shared_secret, iv, ciphertext):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode())
    key = sha1.digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv))
    return unpad(cipher.decrypt(bytes.fromhex(ciphertext)), 16).decode()


r.recvuntil(b"Intercepted from Alice: ")
alice_data = json.loads(r.recvline().decode())
p = int(alice_data['p'], 16)
g = int(alice_data['g'], 16)
A = int(alice_data['A'], 16)


# We send A = p to Bob, so shared secret = p^b mod p = 0
msg_to_bob = {
    "p": hex(p),
    "g": hex(g),
    "A": hex(p)
}
r.sendlineafter(b"Send to Bob: ", json.dumps(msg_to_bob).encode())


r.recvuntil(b"Intercepted from Bob: ")
bob_data = json.loads(r.recvline().decode())
iv = bob_data['iv']
ciphertext = bob_data['encrypted_flag']


print(decrypt_flag(0, iv, ciphertext))
