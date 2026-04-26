import requests

def solve():
    print("[*] Đang tải dữ liệu mã hóa từ CryptoHack...")
    try:
        r = requests.get('https://aes.cryptohack.org/bean_counter/encrypt/')
        encrypted_hex = r.json()['encrypted']
        encrypted_bytes = bytes.fromhex(encrypted_hex)
    except Exception as e:
        print(f"[-] Lỗi khi tải dữ liệu: {e}")
        return

    png_header = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52])
    
    c0 = encrypted_bytes[:16]
    
    keystream = bytes(a ^ b for a, b in zip(c0, png_header))
    decrypted_bytes = bytearray()
    
    for i in range(0, len(encrypted_bytes), 16):
        block = encrypted_bytes[i:i+16]
        decrypted_block = bytes(a ^ b for a, b in zip(block, keystream))
        decrypted_bytes.extend(decrypted_block)
        
    output_filename = 'bean_flag_decrypted.png'
    with open(output_filename, 'wb') as f:
        f.write(decrypted_bytes)
        
    print(f"[+] Thành công! Hãy mở file '{output_filename}' trong thư mục hiện tại để đọc flag.")

if __name__ == '__main__':
    solve()