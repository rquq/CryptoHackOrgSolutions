from pwn import *
import json
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


r = remote('socket.cryptohack.org', 13378)


def decrypt_flag(shared_secret, iv, ciphertext):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode())
    key = sha1.digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv))
    try:
        return unpad(cipher.decrypt(bytes.fromhex(ciphertext)), 16).decode()
    except:
        return None


r.recvuntil(b"Intercepted from Alice: ")
alice_params = json.loads(r.recvline().decode())
p = int(alice_params['p'], 16)


# MITM: Force g = p - 1, which has order 2
alice_params['g'] = hex(p - 1)
alice_params['A'] = hex(p - 1)
r.sendlineafter(b"Send to Bob: ", json.dumps(alice_params).encode())


r.recvuntil(b"Intercepted from Bob: ")
bob_data = json.loads(r.recvline().decode())
iv = bob_data['iv']
ciphertext = bob_data['encrypted_flag']


# Shared secret can only be 1 or p-1
for s in [1, p - 1]:
    res = decrypt_flag(s, iv, ciphertext)
    if res:
        print(res)
        break
