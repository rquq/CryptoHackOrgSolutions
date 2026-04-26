import asyncio
import aiohttp
from collections import Counter

url = "https://aes.cryptohack.org/oh_snap/send_cmd/00/"

async def fetch(session, nonce, i):
    """Hàm gửi truy vấn bất đồng bộ"""
    async with session.get(url + nonce) as response:
        res = await response.json()
        return i, res

async def main():
    flag = ""
    async with aiohttp.ClientSession() as session:
        while True:
            idx = len(flag)
            counts = Counter()
            tasks = []
            for i in range(256):
                nonce = bytes([idx + 3, 255, i]).hex()
                tasks.append(asyncio.create_task(fetch(session, nonce, i)))
            results = await asyncio.gather(*tasks)
            for i, res in results:
                if "error" in res:
                    cmd_hex = res["error"].split(": ")[1]
                    keystream_byte = bytes.fromhex(cmd_hex)[0]
                    
                    S = list(range(256))
                    j = 0
                    K = bytes([idx + 3, 255, i]) + flag.encode()
                    
                    for step in range(idx + 3):
                        j = (j + S[step] + K[step]) % 256
                        S[step], S[j] = S[j], S[step]
                    
                    guess = (keystream_byte - j - S[idx + 3]) % 256
                    counts[guess] += 1
                    
            if not counts:
                print("Lỗi: Không thu thập được dữ liệu.")
                break
            flag += chr(counts.most_common(1)[0][0])
            print(f"Cờ hiện tại: {flag}")
            
            if flag.endswith("}"):
                print("\nHoàn thành!")
                break

if __name__ == "__main__":
    asyncio.run(main())