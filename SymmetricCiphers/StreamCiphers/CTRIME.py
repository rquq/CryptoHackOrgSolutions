import requests
import string
import sys

def solve():
    url = "https://aes.cryptohack.org/ctrime/encrypt/"
    charset = string.ascii_letters + string.digits + "{}_!?"
    flag = "crypto{"
    
    while not flag.endswith("}"):
        min_len = 999999
        best_chars = []
        
        for c in charset:
            test_str = flag + c
            test_hex = test_str.encode().hex()
            
            try:
                r = requests.get(f"{url}{test_hex}/")
                data = r.json()
                
                if "ciphertext" in data:
                    ct_len = len(data["ciphertext"])
                    
                    if ct_len < min_len:
                        min_len = ct_len
                        best_chars = [c]
                    elif ct_len == min_len:
                        best_chars.append(c)
            except Exception:
                sys.exit(1)
                
        if best_chars:
            flag += best_chars[0]
            print(flag)
        else:
            break

if __name__ == '__main__':
    solve()