import requests

URL = "http://aes.cryptohack.org/paper_plane/"

def encrypt_msg():
    res = requests.get(f"{URL}encrypt_msg/")
    return bytes.fromhex(res.json()["ciphertext"])

def oracle(ct):
    res = requests.get(f"{URL}send_msg/{ct.hex()}/")
    return "error" not in res.json()

def decrypt_block(m0, c0, c1):
    intermediate = bytearray(16)
    for i in range(1, 17):
        for guess in range(256):
            c0_prime = bytearray(16)
            for j in range(1, i):
                c0_prime[16-j] = intermediate[16-j] ^ i
            
            c0_prime[16-i] = guess
            test_ct = m0 + bytes(c0_prime) + c1
            
            if oracle(test_ct):
                intermediate[16-i] = guess ^ i
                break
                
    return bytes([intermediate[k] ^ c0[k] for k in range(16)])

def solve():
    ct = encrypt_msg()
    blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]
    
    m0 = blocks[0]
    c0 = blocks[1]
    c_blocks = blocks[2:]
    
    flag = b""
    prev_m = m0
    prev_c = c0
    
    for c_block in c_blocks:
        pt_block = decrypt_block(prev_m, prev_c, c_block)
        flag += pt_block
        prev_m = pt_block
        prev_c = c_block
        
    print(flag.decode(errors='ignore'))

if __name__ == "__main__":
    solve()