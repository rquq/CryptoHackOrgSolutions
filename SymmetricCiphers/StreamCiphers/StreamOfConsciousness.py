import requests
import string

def solve():
    url = "https://aes.cryptohack.org/stream_consciousness/encrypt/"
    ciphertexts = set()
    
    for _ in range(100):
        try:
            r = requests.get(url)
            ct = bytes.fromhex(r.json()["ciphertext"])
            ciphertexts.add(ct)
        except Exception:
            continue
            
    ciphertexts = list(ciphertexts)
    max_len = max(len(ct) for ct in ciphertexts)
    keystream = bytearray(max_len)
    
    for i in range(max_len):
        best_k = 0
        best_score = -999999
        
        for k in range(256):
            score = 0
            for ct in ciphertexts:
                if i < len(ct):
                    c = chr(ct[i] ^ k)
                    if c in string.ascii_letters:
                        score += 10
                    elif c == ' ':
                        score += 20
                    elif c in string.digits + '_{}!?.\',;-':
                        score += 5
                    elif c in string.printable:
                        score += 1
                    else:
                        score -= 50
            
            if score > best_score:
                best_score = score
                best_k = k
                
        keystream[i] = best_k
        
    for ct in ciphertexts:
        pt = bytes(c ^ k for c, k in zip(ct, keystream)).decode(errors='ignore')
        if 'crypto{' in pt:
            print(pt)

if __name__ == '__main__':
    solve()