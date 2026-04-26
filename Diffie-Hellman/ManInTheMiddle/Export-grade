from pwn import *
import json
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


r = remote('socket.cryptohack.org', 13379)


def decrypt_flag(shared_secret, iv, ciphertext):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode())
    key = sha1.digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv))
    return unpad(cipher.decrypt(bytes.fromhex(ciphertext)), 16).decode()


r.recvuntil(b"Intercepted from Alice: ")
alice_params = json.loads(r.recvline().decode())


# MITM: Force g = 1 so shared secret is always 1
alice_params['g'] = hex(1)
r.sendlineafter(b"Send to Bob: ", json.dumps(alice_params).encode())


r.recvuntil(b"Intercepted from Bob: ")
# Forward Bob's response (B = 1^b = 1)
r.sendlineafter(b"Send to Alice: ", r.recvline())


r.recvuntil(b"Intercepted from Alice: ")
# A = 1^a = 1
r.sendlineafter(b"Send to Bob: ", r.recvline())


r.recvuntil(b"Intercepted from Alice: ")
encrypted_data = json.loads(r.recvline().decode())


print(decrypt_flag(1, encrypted_data['iv'], encrypted_data['encrypted_flag']))
