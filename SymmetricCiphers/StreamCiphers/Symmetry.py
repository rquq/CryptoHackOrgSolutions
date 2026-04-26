import requests

def solve():
    url_flag = 'https://aes.cryptohack.org/symmetry/encrypt_flag/'
    r1 = requests.get(url_flag).json()
    c = r1['ciphertext']
    
    iv = c[:32]
    encrypted_flag = c[32:]
    
    url_decrypt = f'https://aes.cryptohack.org/symmetry/encrypt/{encrypted_flag}/{iv}/'
    r2 = requests.get(url_decrypt).json()
    
    flag_hex = r2['ciphertext']
    flag = bytes.fromhex(flag_hex).decode()
    
    print(flag)

if __name__ == '__main__':
    solve()