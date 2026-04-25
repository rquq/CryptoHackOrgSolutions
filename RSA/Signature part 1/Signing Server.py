from Crypto.Util.number import  bytes_to_long as btl
from Crypto.Util.number import long_to_bytes as ltb
import socket, json


with socket.create_connection(("socket.cryptohack.org", 13374)) as s, s.makefile('rw') as f:
    f.readline()
   
    f.write('{"option": "get_secret"}\n')
    f.flush()
    secret = json.loads(f.readline())["secret"]
   
    f.write(json.dumps({"option": "sign", "msg": secret[2:]}) + '\n')
    f.flush()
    sig = json.loads(f.readline())["signature"]
   
    print(ltb(int(sig, 16)))
