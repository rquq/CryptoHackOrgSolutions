import socket
import json
import time

def solve():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("socket.cryptohack.org", 13399))
            f = s.makefile('rw')
            f.readline()
            
            while True:
                f.write(json.dumps({"option": "reset_connection"}) + '\n')
                f.flush()
                f.readline()
                
                f.write(json.dumps({"option": "reset_password", "token": "00" * 28}) + '\n')
                f.flush()
                f.readline()
                
                f.write(json.dumps({"option": "authenticate", "password": ""}) + '\n')
                f.flush()
                resp = f.readline()
                
                if not resp:
                    break
                    
                data = json.loads(resp)
                if "crypto{" in data.get("msg", ""):
                    print(data["msg"])
                    return
        except Exception:
            time.sleep(1)
            continue

if __name__ == '__main__':
    solve()