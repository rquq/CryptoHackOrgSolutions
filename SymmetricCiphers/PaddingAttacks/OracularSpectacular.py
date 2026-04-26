#!/usr/bin/env python3
import json
import socket
import time
from collections import Counter

HOST = "socket.cryptohack.org"
PORT = 13423

def recv_json(s):
    buf = b""
    while True:
        chunk = s.recv(4096)
        buf += chunk
        text = buf.decode(errors='ignore').strip()
        for line in text.split('\n'):
            line = line.strip()
            if line:
                try:
                    return json.loads(line)
                except:
                    pass

def send_json(s, obj):
    s.sendall((json.dumps(obj) + "\n").encode())

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(15)
    s.connect((HOST, PORT))
    time.sleep(0.3)
    try:
        s.recv(4096)
    except:
        pass
    return s

def get_ct(s):
    send_json(s, {"option": "encrypt"})
    r = recv_json(s)
    return bytes.fromhex(r["ct"])

def check_padding_once(s, ct: bytes) -> bool:
    send_json(s, {"option": "unpad", "ct": ct.hex()})
    r = recv_json(s)
    return r.get("result", False)

def check_padding_voted(s, ct: bytes, n: int) -> float:
    """Query n times, return fraction of True responses."""
    true_count = 0
    for _ in range(n):
        if check_padding_once(s, ct):
            true_count += 1
    return true_count / n

def padding_oracle_attack(s, iv: bytes, ct_block: bytes) -> bytes:
    """
    Oracle lies with p=0.6, tells truth with p=0.4.
    So: P(result=True | padding valid)   = 0.4
        P(result=True | padding invalid) = 0.6
    
    We query multiple times. Valid padding → lower True rate.
    Invalid padding → higher True rate.
    Find the guess with LOWEST True rate.
    
    Budget: 12000 queries, 16 bytes.
    Per byte: 12000/16 = 750 queries.
    Per guess: 750/256 ≈ 2-3 queries → too noisy.
    
    Better: Use elimination. Query each guess 3 times,
    pick candidate with lowest True count.
    750 queries/byte, 256 guesses × 3 = 768... tight.
    Use 2 queries per guess first pass (512), then verify top candidates.
    """
    intermediate = bytearray(16)
    total_queries = [0]

    for byte_idx in range(15, -1, -1):
        pad_byte = 16 - byte_idx
        print(f"\n[Byte {byte_idx:2d}] pad_byte={pad_byte}, queries used: {total_queries[0]}")
        
        scores = {}  # guess -> true_count out of N queries
        N = 3  # queries per guess, first pass
        
        for guess in range(256):
            fake_iv = bytearray(16)
            for k in range(byte_idx + 1, 16):
                fake_iv[k] = intermediate[k] ^ pad_byte
            fake_iv[byte_idx] = guess
            fake_ct = bytes(fake_iv) + ct_block
            
            true_count = 0
            for _ in range(N):
                if check_padding_once(s, fake_ct):
                    true_count += 1
            scores[guess] = true_count
            total_queries[0] += N

        # Valid padding → oracle returns True 40% → lowest score
        # Invalid → 60% True → higher score
        # Sort by score ascending → first candidates are likely valid
        sorted_guesses = sorted(scores.items(), key=lambda x: x[1])
        
        # Top candidates with lowest score (more likely valid padding)
        top_candidates = [g for g, sc in sorted_guesses if sc <= sorted_guesses[0][1]]
        
        # If tie, take all with score 0 first, then 1, etc.
        # Do extra verification on top 5 candidates
        verify_N = 10
        best_guess = None
        best_score = 999
        
        for guess, _ in sorted_guesses[:5]:
            fake_iv = bytearray(16)
            for k in range(byte_idx + 1, 16):
                fake_iv[k] = intermediate[k] ^ pad_byte
            fake_iv[byte_idx] = guess
            fake_ct = bytes(fake_iv) + ct_block
            
            true_count = sum(check_padding_once(s, fake_ct) for _ in range(verify_N))
            total_queries[0] += verify_N
            
            if true_count < best_score:
                best_score = true_count
                best_guess = guess

        intermediate[byte_idx] = best_guess ^ pad_byte
        print(f"  → intermediate[{byte_idx}] = 0x{intermediate[byte_idx]:02x} "
              f"(guess=0x{best_guess:02x}, score={best_score}/{verify_N})")

    plaintext = bytes([intermediate[i] ^ iv[i] for i in range(16)])
    print(f"\nTotal queries used: {total_queries[0]}")
    return plaintext

def main():
    s = connect()
    print("Getting ciphertext...")
    ct_full = get_ct(s)
    iv = ct_full[:16]
    ct_block = ct_full[16:]
    print(f"IV:  {iv.hex()}")
    print(f"CT:  {ct_block.hex()}")

    print("\nRunning noisy padding oracle attack...")
    pt = padding_oracle_attack(s, iv, ct_block)
    
    try:
        message = pt.decode("ascii")
        print(f"\nRecovered message: {message}")
    except Exception as e:
        print(f"Decode error: {e}, raw: {pt.hex()}")
        return

    print("Submitting message...")
    send_json(s, {"option": "check", "message": message})
    r = recv_json(s)
    print(f"Result: {r}")

if __name__ == "__main__":
    main()