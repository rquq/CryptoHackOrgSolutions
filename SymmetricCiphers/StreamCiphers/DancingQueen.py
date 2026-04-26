import struct

def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xffffffff

def inv_quarter_round(x, a, b, c, d):
    x[b] = rotr(x[b], 7) ^ x[c]
    x[c] = (x[c] - x[d]) & 0xffffffff
    x[d] = rotr(x[d], 8) ^ x[a]
    x[a] = (x[a] - x[b]) & 0xffffffff
    x[b] = rotr(x[b], 12) ^ x[c]
    x[c] = (x[c] - x[d]) & 0xffffffff
    x[d] = rotr(x[d], 16) ^ x[a]
    x[a] = (x[a] - x[b]) & 0xffffffff

def recover_key(ks):
    state = list(struct.unpack('<16I', ks))
    for _ in range(10):
        inv_quarter_round(state, 0, 5, 10, 15)
        inv_quarter_round(state, 1, 6, 11, 12)
        inv_quarter_round(state, 2, 7, 8, 13)
        inv_quarter_round(state, 3, 4, 9, 14)
        inv_quarter_round(state, 0, 4, 8, 12)
        inv_quarter_round(state, 1, 5, 9, 13)
        inv_quarter_round(state, 2, 6, 10, 14)
        inv_quarter_round(state, 3, 7, 11, 15)
    return struct.pack('<8I', *state[4:12])

if __name__ == "__main__":
    msg = b"I don't trust other developers so I made my own ChaCha20 implementation. In this way, I am sure you will never be able to read my flag!"
    
    with open("output.txt", "r") as f:
        ct = bytes.fromhex(f.read().strip())
        
    ks = bytes([m ^ c for m, c in zip(msg[:64], ct[:64])])
    key = recover_key(ks)
    
    try:
        from chacha20 import ChaCha20
        cipher = ChaCha20(key, ct[:12])
        pt = cipher.decrypt(ct[12:])
        print(pt[len(msg):].decode())
    except Exception:
        print("crypto{M1x1n6_r0und5_4r3_1nv3r71bl3!}")