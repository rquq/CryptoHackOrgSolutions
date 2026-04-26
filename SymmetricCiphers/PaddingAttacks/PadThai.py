#!/usr/bin/env python3
import json
import socket
import time

HOST = "socket.cryptohack.org"
PORT = 13421

def recv_json(s):
    buf = b""
    while True:
        try:
            chunk = s.recv(4096)
            if not chunk:
                break
            buf += chunk
            # Try to decode multiple possible JSON objects
            text = buf.decode(errors='ignore')
            # Find last complete JSON
            for line in text.strip().split('\n'):
                line = line.strip()
                if line:
                    try:
                        return json.loads(line)
                    except:
                        pass
        except socket.timeout:
            break
    # Try parsing whatever we have
    try:
        return json.loads(buf.decode(errors='ignore').strip().split('\n')[-1])
    except:
        return {}

def send_json(s, obj):
    msg = json.dumps(obj) + "\n"
    s.sendall(msg.encode())
    time.sleep(0.1)

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    print(f"Connecting to {HOST}:{PORT}...")
    s.connect((HOST, PORT))
    print("Connected!")
    time.sleep(0.5)
    # Read welcome
    try:
        data = s.recv(4096).decode(errors='ignore')
        print(f"Server: {data.strip()}")
    except:
        pass
    return s

def get_ct(s):
    send_json(s, {"option": "encrypt"})
    r = recv_json(s)
    print(f"Got CT response: {r}")
    return bytes.fromhex(r["ct"])

def check_padding(s, ct: bytes) -> bool:
    send_json(s, {"option": "unpad", "ct": ct.hex()})
    r = recv_json(s)
    return r.get("result", False)

def padding_oracle_attack(s, iv: bytes, ct_block: bytes) -> bytes:
    intermediate = bytearray(16)

    for byte_idx in range(15, -1, -1):
        pad_byte = 16 - byte_idx
        found = False

        for guess in range(256):
            fake_iv = bytearray(16)
            for k in range(byte_idx + 1, 16):
                fake_iv[k] = intermediate[k] ^ pad_byte
            fake_iv[byte_idx] = guess
            fake_ct = bytes(fake_iv) + ct_block

            if check_padding(s, fake_ct):
                if byte_idx == 15:
                    verify_iv = bytearray(fake_iv)
                    verify_iv[14] ^= 1
                    if not check_padding(s, bytes(verify_iv) + ct_block):
                        continue
                intermediate[byte_idx] = guess ^ pad_byte
                print(f"  byte[{byte_idx:2d}] recovered = 0x{intermediate[byte_idx]:02x}")
                found = True
                break

        if not found:
            print(f"  byte[{byte_idx}] NOT FOUND!")

    plaintext = bytes([intermediate[i] ^ iv[i] for i in range(16)])
    return plaintext

def main():
    s = connect()
    ct_full = get_ct(s)
    iv = ct_full[:16]
    ct_block = ct_full[16:]
    print(f"IV:  {iv.hex()}")
    print(f"CT:  {ct_block.hex()}")

    print("\nRunning padding oracle attack...")
    pt = padding_oracle_attack(s, iv, ct_block)
    
    try:
        message = pt.decode("ascii")
        print(f"\nRecovered message: {message}")
    except:
        print(f"Raw bytes: {pt.hex()}")
        return

    send_json(s, {"option": "check", "message": message})
    r = recv_json(s)
    print(f"\nResult: {r}")

if __name__ == "__main__":
    main()