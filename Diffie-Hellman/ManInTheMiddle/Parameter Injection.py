from pwn import *
import json
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


r = remote('socket.cryptohack.org', 13371)


def decrypt_flag(shared_secret, iv, ciphertext):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode())
    key = sha1.digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv))
    return unpad(cipher.decrypt(bytes.fromhex(ciphertext)), 16)


r.recvuntil(b"Intercepted from Alice: ")
alice_data = json.loads(r.recvline().decode())
p = int(alice_data['p'], 16)


# Send p to Bob so his B becomes 0
alice_data['g'] = hex(p)
alice_data['A'] = hex(p)
r.sendlineafter(b"Send to Bob: ", json.dumps(alice_data).encode())


r.recvuntil(b"Intercepted from Bob: ")
bob_data = json.loads(r.recvline().decode())


# Send p back to Alice so her shared secret becomes 0
bob_data['B'] = hex(p)
r.sendlineafter(b"Send to Alice: ", json.dumps(bob_data).encode())


r.recvuntil(b"Intercepted from Alice: ")
encrypted_data = json.loads(r.recvline().decode())


iv = encrypted_data['iv']
ciphertext = encrypted_data['encrypted_flag']
print(decrypt_flag(0, iv, ciphertext).decode())
