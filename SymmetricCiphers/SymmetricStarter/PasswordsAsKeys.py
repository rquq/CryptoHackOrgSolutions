import requests
import hashlib
from Crypto.Cipher import AES

res = requests.get('https://aes.cryptohack.org/passwords_as_keys/encrypt_flag')
ciphertext = bytes.fromhex(res.json()["ciphertext"])

words_url = 'https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words'
words = requests.get(words_url).text.splitlines()

for word in words:
    key = bytes.fromhex(hashlib.md5(word.encode()).hexdigest())
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    if b'crypto{' in decrypted:
        print(decrypted)
        break