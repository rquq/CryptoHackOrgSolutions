from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long
from os import urandom
from pwn import remote
import json
import binascii
import time

r=remote('socket.cryptohack.org',13399)
data = r.recvline()
print(data)
time.sleep(0.01)

i=1
while True:
    print(f'Conection {i}th:')
    i+=1
    your_input={'option':'reset_connection'}
    to_send = json.dumps(your_input)
    r.send(to_send)
    data = r.recvline()
    data = json.loads(data)
    if 'Connection has been reset.' in data['msg']:
        print("Connection has been reset.")
    else:
        print(data)
        break
    time.sleep(0.01)

    ciphertext=''
    ciphertext+='00'*16 #IV
    ciphertext+='00'*8 #password
    ciphertext+='00'*3 #len password (3 bytes)
    ciphertext+='08' #len password (1 byte)
    token= ciphertext
    your_input={'option':'reset_password','token':token}
    to_send = json.dumps(your_input)
    r.send(to_send)
    data = r.recvline()
    data = json.loads(data)
    if 'Password has been correctly reset.' in data['msg']:
        print("Password has been correctly reset.")
    else:
        print(data)
        break
    time.sleep(0.01)

    password='\x00'*8
    your_input={'option':'authenticate','password':password}
    to_send = json.dumps(your_input)
    r.send(to_send)
    data = r.recvline()
    data = json.loads(data)
    if 'Welcome admin,' in data['msg']:
        print(data['msg'])
        break
    time.sleep(0.01)